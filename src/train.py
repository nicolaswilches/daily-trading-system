import polars as pl
import os
import joblib
import optuna
import lightgbm as lgb
from sklearn.metrics import precision_score, root_mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
import numpy as np

def get_feature_list(df):
    """Automatically identify numeric features, excluding targets and metadata."""
    exclude = ["Ticker", "Date", "SimFinId", "Target_Is_Up", "Target_Log_Return"]
    # Only include numeric columns (Int, Float)
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
    
    features = get_feature_list(df)
    print(f"Total features identified: {len(features)}")
    
    X = df.select(features).to_pandas().values
    y_class = df["Target_Is_Up"].to_pandas().values
    y_reg = df["Target_Log_Return"].to_pandas().values
    
    # 1. Classification Tuning
    print("Optimizing Classifier (LightGBM + Optuna)...")
    study_clf = optuna.create_study(direction="maximize")
    study_clf.optimize(lambda trial: objective_classification(trial, X, y_class), n_trials=30)
    
    print("Training Final Classifier with all features...")
    best_clf = lgb.LGBMClassifier(**study_clf.best_params, verbosity=-1)
    best_clf.fit(X, y_class)
    
    # 2. Regression Tuning
    print("Optimizing Regressor (LightGBM + Optuna)...")
    study_reg = optuna.create_study(direction="minimize")
    study_reg.optimize(lambda trial: objective_regression(trial, X, y_reg), n_trials=30)
    
    print("Training Final Regressor with all features...")
    best_reg = lgb.LGBMRegressor(**study_reg.best_params, verbosity=-1)
    best_reg.fit(X, y_reg)
    
    # 3. Save everything
    os.makedirs("models", exist_ok=True)
    joblib.dump(best_clf, "models/classifier.joblib")
    joblib.dump(best_reg, "models/regressor.joblib")
    joblib.dump(features, "models/features_list.joblib")
    
    print("\nTraining Complete!")
    print(f"Features used: {len(features)}")
    print(f"Best Class Precision (CV): {study_clf.best_value:.4f}")
    print(f"Best Reg RMSE (CV): {study_reg.best_value:.4f}")
    
    # Print top 5 features for the classifier to see what it liked
    import matplotlib.pyplot as plt
    lgb.plot_importance(best_clf, max_num_features=10)
    plt.title("Top Features (Classifier)")
    plt.show()

if __name__ == "__main__":
    train_and_optimize()
