import polars as pl
import os
import joblib
from xgboost import XGBClassifier, XGBRegressor
from sklearn.metrics import classification_report, mean_absolute_error, root_mean_squared_error, precision_score, recall_score
import pandas as pd

def train_models(input_path):
    print(f"Loading features from {input_path}...")
    df = pl.read_parquet(input_path)
    
    # Sort by date for time-series split
    df = df.sort("Date")
    
    # Features (X) and Targets (y)
    # Exclude non-feature columns and targets
    exclude = ["Ticker", "Date", "Target_Is_Up", "Target_Next_Price", "Ticker_Symbol"]
    features = [c for c in df.columns if c not in exclude]
    
    X = df.select(features).to_pandas()
    y_class = df["Target_Is_Up"].to_pandas()
    y_reg = df["Target_Next_Price"].to_pandas()
    
    # Time Series Split (80/20 approximately)
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_class_train, y_class_test = y_class.iloc[:split_idx], y_class.iloc[split_idx:]
    y_reg_train, y_reg_test = y_reg.iloc[:split_idx], y_reg.iloc[split_idx:]
    
    print(f"Training Classification Model (XGBoost)...")
    clf = XGBClassifier(n_estimators=100, learning_rate=0.05, max_depth=5, random_state=42)
    clf.fit(X_train, y_class_train)
    
    print(f"Training Regression Model (XGBoost)...")
    reg = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5, random_state=42)
    reg.fit(X_train, y_reg_train)
    
    # Evaluation - Classification
    y_class_pred = clf.predict(X_test)
    print("\n--- Classification Performance (Up/Down) ---")
    print(f"Precision: {precision_score(y_class_test, y_class_pred):.4f}")
    print(f"Recall: {recall_score(y_class_test, y_class_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_class_test, y_class_pred))
    
    # Evaluation - Regression
    y_reg_pred = reg.predict(X_test)
    print("\n--- Regression Performance (Price) ---")
    print(f"MAE: {mean_absolute_error(y_reg_test, y_reg_pred):.4f}")
    print(f"RMSE: {root_mean_squared_error(y_reg_test, y_reg_pred):.4f}")
    
    # Save Models
    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, "models/classifier.joblib")
    joblib.dump(reg, "models/regressor.joblib")
    joblib.dump(features, "models/features_list.joblib")
    print("\nModels and features list saved to models/ folder.")

if __name__ == "__main__":
    train_models("data/processed/features.parquet")
