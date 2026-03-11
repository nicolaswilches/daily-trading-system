import polars as pl
import os

def process_data(input_path, output_path):
    print(f"Loading data from {input_path}...")
    df = pl.read_parquet(input_path)
    
    # Sort and Clean
    df = df.sort(["Ticker", "Date"])
    
    # Ensure types
    if df.schema["Date"] == pl.String:
        df = df.with_columns(pl.col("Date").str.strptime(pl.Date, "%Y-%m-%d"))
        
    df = df.with_columns([
        pl.col("Close").cast(pl.Float64),
        pl.col("Open").cast(pl.Float64),
        pl.col("High").cast(pl.Float64),
        pl.col("Low").cast(pl.Float64),
        pl.col("Volume").cast(pl.Float64),
        pl.col("Dividend").fill_null(0.0).cast(pl.Float64),
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

    # Drop rows with nulls in key feature/target columns
    # We drop nulls in SMA_50 because it's our largest window
    # We drop nulls in Target_Is_Up because it's our prediction target
    df = df.drop_nulls(subset=["SMA_50", "Target_Is_Up"])
    
    print(f"Saving processed features to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.write_parquet(output_path)
    print(f"Final feature set size: {len(df)}")

if __name__ == "__main__":
    process_data("data/raw/prices.parquet", "data/processed/features.parquet")
