import polars as pl
import os
import joblib
import optuna
import lightgbm as lgb
from sklearn.metrics import precision_score, root_mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
import numpy as np

HOLDOUT_FRACTION = 0.20


def get_feature_list(df):
    """Automatically identify numeric features, excluding targets and metadata."""
    exclude = ["Ticker", "Date", "SimFinId", "Target_Is_Up", "Target_Log_Return"]
    numeric_cols = [c for c, t in df.schema.items() if t in [pl.Int64, pl.Float64, pl.Int32, pl.Float32]]
    return [c for c in numeric_cols if c not in exclude]


def objective_classification(trial, X, y):
    param = {
        "objective": "binary",
        "metric": "binary_logloss",
        "verbosity": -1,
        "boosting_type": "gbdt",
        "learning_rate": trial.suggest_float("learning_rate", 0.005, 0.1, log=True),
        "n_estimators": trial.suggest_int("n_estimators", 50, 500),
        "num_leaves": trial.suggest_int("num_leaves", 20, 100),
        "max_depth": trial.suggest_int("max_depth", 3, 12),
        "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 5, 100),
        "feature_fraction": trial.suggest_float("feature_fraction", 0.4, 1.0),
        "lambda_l1": trial.suggest_float("lambda_l1", 1e-8, 10.0, log=True),
        "lambda_l2": trial.suggest_float("lambda_l2", 1e-8, 10.0, log=True),
    }

    tscv = TimeSeriesSplit(n_splits=5)
    precisions = []

    for train_idx, val_idx in tscv.split(X):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]

        clf = lgb.LGBMClassifier(**param)
        clf.fit(X_train, y_train)
        preds = clf.predict(X_val)
        precisions.append(precision_score(y_val, preds, zero_division=0))

    return np.mean(precisions)


def objective_regression(trial, X, y):
    param = {
        "objective": "regression",
        "metric": "rmse",
        "verbosity": -1,
        "learning_rate": trial.suggest_float("learning_rate", 0.005, 0.1, log=True),
        "n_estimators": trial.suggest_int("n_estimators", 50, 500),
        "num_leaves": trial.suggest_int("num_leaves", 20, 100),
        "max_depth": trial.suggest_int("max_depth", 3, 12),
        "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 5, 100),
        "feature_fraction": trial.suggest_float("feature_fraction", 0.4, 1.0),
    }

    tscv = TimeSeriesSplit(n_splits=5)
    rmses = []

    for train_idx, val_idx in tscv.split(X):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]

        reg = lgb.LGBMRegressor(**param)
        reg.fit(X_train, y_train)
        preds = reg.predict(X_val)
        rmses.append(root_mean_squared_error(y_val, preds))

    return np.mean(rmses)


def train_and_optimize():
    print("Loading all features from ETL...")
    df = pl.read_parquet("data/processed/features.parquet").sort("Date")

    # Chronological train/holdout split — prevents data leakage.
    # Holdout is the last HOLDOUT_FRACTION of unique dates so every ticker
    # contributes its most recent window to the out-of-sample evaluation.
    unique_dates = df["Date"].unique().sort()
    cutoff_idx = int(len(unique_dates) * (1 - HOLDOUT_FRACTION))
    cutoff_date = unique_dates[cutoff_idx]
    df_train = df.filter(pl.col("Date") < cutoff_date)
    df_test = df.filter(pl.col("Date") >= cutoff_date)

    print(f"Train rows: {len(df_train)} | Holdout rows: {len(df_test)}")
    print(f"Train date range: {df_train['Date'].min()} → {df_train['Date'].max()}")
    print(f"Holdout cutoff date: {cutoff_date}")

    features = get_feature_list(df_train)
    print(f"Total features identified: {len(features)}")

    X_train = df_train.select(features).to_pandas().values
    y_class_train = df_train["Target_Is_Up"].to_pandas().values
    y_reg_train = df_train["Target_Log_Return"].to_pandas().values

    # 1. Classification Tuning (CV on train portion only)
    print("Optimizing Classifier (LightGBM + Optuna)...")
    study_clf = optuna.create_study(direction="maximize")
    study_clf.optimize(
        lambda trial: objective_classification(trial, X_train, y_class_train),
        n_trials=30,
    )

    print("Training Final Classifier on train portion only...")
    best_clf = lgb.LGBMClassifier(**study_clf.best_params, verbosity=-1)
    best_clf.fit(X_train, y_class_train)

    # 2. Regression Tuning (CV on train portion only)
    print("Optimizing Regressor (LightGBM + Optuna)...")
    study_reg = optuna.create_study(direction="minimize")
    study_reg.optimize(
        lambda trial: objective_regression(trial, X_train, y_reg_train),
        n_trials=30,
    )

    print("Training Final Regressor on train portion only...")
    best_reg = lgb.LGBMRegressor(**study_reg.best_params, verbosity=-1)
    best_reg.fit(X_train, y_reg_train)

    # 3. Out-of-sample evaluation on holdout
    X_test = df_test.select(features).to_pandas().values
    y_class_test = df_test["Target_Is_Up"].to_pandas().values
    y_reg_test = df_test["Target_Log_Return"].to_pandas().values

    holdout_precision = precision_score(
        y_class_test, best_clf.predict(X_test), zero_division=0
    )
    holdout_rmse = root_mean_squared_error(y_reg_test, best_reg.predict(X_test))

    # 4. Save artifacts
    os.makedirs("models", exist_ok=True)
    joblib.dump(best_clf, "models/classifier.joblib")
    joblib.dump(best_reg, "models/regressor.joblib")
    joblib.dump(features, "models/features_list.joblib")
    joblib.dump(
        {
            "cutoff_date": str(cutoff_date),
            "holdout_fraction": HOLDOUT_FRACTION,
            "train_rows": len(df_train),
            "holdout_rows": len(df_test),
            "cv_precision": float(study_clf.best_value),
            "cv_rmse": float(study_reg.best_value),
            "holdout_precision": float(holdout_precision),
            "holdout_rmse": float(holdout_rmse),
        },
        "models/split_meta.joblib",
    )

    print("\nTraining Complete!")
    print(f"Features used: {len(features)}")
    print(f"CV Precision (train folds): {study_clf.best_value:.4f}")
    print(f"CV RMSE (train folds): {study_reg.best_value:.4f}")
    print(f"Holdout Precision: {holdout_precision:.4f}")
    print(f"Holdout RMSE: {holdout_rmse:.4f}")


if __name__ == "__main__":
    train_and_optimize()
