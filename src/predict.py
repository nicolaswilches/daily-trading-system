import polars as pl
import joblib
import numpy as np
from src.api_wrapper import PySimFin
from datetime import datetime

def run_prediction(ticker):
    """
    Fetches live data (V3), processes it, and returns the full dataset + prediction.
    """
    api = PySimFin()
    
    # SimFin ticker mapping
    search_ticker = ticker
    if ticker == "GOOGL": search_ticker = "GOOG"
    
    # 1. Fetch live data
    try:
        df_prices = api.get_share_prices(search_ticker)
    except Exception as e:
        if "429" in str(e):
            return {"error": "API Limit Reached. Please try again tomorrow (Free tier quota exhausted)."}
        return {"error": f"API Error: {e}"}
    
    if df_prices is None or len(df_prices) < 200:
        return {"error": f"Insufficient data for {ticker} (fetched as {search_ticker})."}
        
    # 2. Cleaning and Sorting
    df = df_prices.with_columns([
        pl.col("Date").str.strptime(pl.Date, "%Y-%m-%d"),
        pl.col("Close").cast(pl.Float64),
        pl.col("Open").cast(pl.Float64),
        pl.col("High").cast(pl.Float64),
        pl.col("Low").cast(pl.Float64),
        pl.col("Volume").cast(pl.Float64),
    ]).sort("Date")
    
    # 3. Apply ETL Logic
    df = df.with_columns([
        (pl.col("Close") / pl.col("Close").shift(1)).log().alias("Log_Return_1d"),
        (pl.col("Close") / pl.col("Close").rolling_mean(20) - 1).alias("Dist_SMA_20"),
        (pl.col("Close") / pl.col("Close").rolling_mean(50) - 1).alias("Dist_SMA_50"),
        (pl.col("Close") / pl.col("Close").rolling_mean(200) - 1).alias("Dist_SMA_200"),
        ((pl.col("Close").diff() > 0).cast(pl.Int32).rolling_mean(14) / 
         (pl.col("Close").diff().abs().rolling_mean(14) + 1e-9)).alias("RSI_Proxy"),
        pl.col("Close").rolling_std(20).alias("Vol_20"),
        (pl.col("High") - pl.col("Low")).rolling_mean(14).alias("ATR_14"),
    ])
    
    # 4. Handle Features
    features_list = joblib.load("models/features_list.joblib")
    for feat in features_list:
        if feat not in df.columns:
            df = df.with_columns(pl.lit(0.0).alias(feat))
            
    # 5. Model Inference
    clf = joblib.load("models/classifier.joblib")
    reg = joblib.load("models/regressor.joblib")
    
    X_latest = df.select(features_list).tail(1).to_pandas().values
    
    prob_up = float(clf.predict_proba(X_latest)[0][1])
    pred_log_return = float(reg.predict(X_latest)[0])
    
    # 6. Result Packaging
    latest = df.tail(1)
    current_price = latest["Close"].item()
    target_price = current_price * np.exp(pred_log_return)
    
    if prob_up > 0.55:
        signal = "BUY"
    elif prob_up < 0.45:
        signal = "SELL"
    else:
        signal = "HOLD"
        
    return {
        "ticker": ticker,
        "current_price": current_price,
        "target_price": target_price,
        "prob_up": prob_up,
        "signal": signal,
        "high": latest["High"].item(),
        "low": latest["Low"].item(),
        "volume": latest["Volume"].item(),
        "change_pct": (np.exp(df["Log_Return_1d"].tail(1).item()) - 1) * 100,
        "last_updated": df["Date"].tail(1).item().strftime("%Y-%m-%d"),
        "history": df # Return the full dataframe for charts
    }
