import polars as pl
import os

def calculate_rsi(series, period=14):
    """Calculate the Relative Strength Index (RSI)."""
    delta = series.diff()
    gain = delta.map_elements(lambda x: x if x > 0 else 0, return_dtype=pl.Float64)
    loss = delta.map_elements(lambda x: -x if x < 0 else 0, return_dtype=pl.Float64)
    
    avg_gain = gain.rolling_mean(window_size=period)
    avg_loss = loss.rolling_mean(window_size=period)
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def process_data(input_path, output_path):
    print(f"Loading data from {input_path}...")
    df = pl.read_parquet(input_path)
    
    # Sort and Clean
    df = df.sort(["Ticker", "Date"])
    
    # Ensure types
    df = df.with_columns([
        pl.col("Date").str.strptime(pl.Date, "%Y-%m-%d"),
        pl.col("Close").cast(pl.Float64),
        pl.col("Open").cast(pl.Float64),
        pl.col("High").cast(pl.Float64),
        pl.col("Low").cast(pl.Float64),
        pl.col("Volume").cast(pl.Float64),
    ])

    print("Calculating features...")
    df = df.with_columns([
        # Moving Averages
        pl.col("Close").rolling_mean(window_size=5).over("Ticker").alias("SMA_5"),
        pl.col("Close").rolling_mean(window_size=20).over("Ticker").alias("SMA_20"),
        pl.col("Close").rolling_mean(window_size=50).over("Ticker").alias("SMA_50"),
        
        # Volatility (Rolling Std Dev)
        pl.col("Close").rolling_std(window_size=20).over("Ticker").alias("Volatility_20"),
        
        # Daily Returns
        (pl.col("Close") / pl.col("Close").shift(1).over("Ticker") - 1).alias("Return_1d"),
    ])

    # Targets (Next day movement and price)
    df = df.with_columns([
        pl.col("Close").shift(-1).over("Ticker").alias("Target_Next_Price"),
    ])
    
    df = df.with_columns([
        (pl.col("Target_Next_Price") > pl.col("Close")).cast(pl.Int64).alias("Target_Is_Up")
    ])

    # Drop rows with nulls (due to rolling windows and shift)
    df = df.drop_nulls()
    
    print(f"Saving processed features to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.write_parquet(output_path)
    print(f"Final feature set size: {len(df)}")

if __name__ == "__main__":
    process_data("data/raw/prices.parquet", "data/processed/features.parquet")
