import polars as pl
import os

def process_all_companies(data_dir="data/raw", output_path="data/processed/features.parquet"):
    print("Loading raw datasets...")
    df_prices = pl.read_parquet(f"{data_dir}/prices.parquet")
    df_income = pl.read_parquet(f"{data_dir}/income.parquet")
    df_balance = pl.read_parquet(f"{data_dir}/balance.parquet")
    df_meta = pl.read_parquet(f"{data_dir}/companies.parquet")

    # 1. Prepare Fundamentals (Quarterly)
    # Align Income and Balance on Ticker and Report Date
    df_fund = df_income.join(
        df_balance, 
        on=["Ticker", "Report Date"], 
        suffix="_bal"
    ).sort(["Ticker", "Publish Date"])

    # 2. Process each ticker to avoid cross-contamination
    all_processed = []
    tickers = df_prices["Ticker"].unique().to_list()

    for ticker in tickers:
        print(f"Processing {ticker}...")
        # Filter ticker-specific data
        p = df_prices.filter(pl.col("Ticker") == ticker).sort("Date")
        f = df_fund.filter(pl.col("Ticker") == ticker).sort("Publish Date")
        
        # Point-in-Time Join: Daily prices + Latest public fundamentals
        df_ticker = p.join_asof(
            f,
            left_on="Date",
            right_on="Publish Date",
            by="Ticker"
        )

        # 3. Indicator Battery (Technical + Fundamental)
        df_ticker = df_ticker.with_columns([
            # Normalization
            (pl.col("Close") / pl.col("Close").shift(1)).log().alias("Log_Return_1d"),
            
            # Trend (Distance from SMAs)
            (pl.col("Close") / pl.col("Close").rolling_mean(20) - 1).alias("Dist_SMA_20"),
            (pl.col("Close") / pl.col("Close").rolling_mean(50) - 1).alias("Dist_SMA_50"),
            (pl.col("Close") / pl.col("Close").rolling_mean(200) - 1).alias("Dist_SMA_200"),
            
            # Momentum (RSI - Relative Strength)
            ((pl.col("Close").diff() > 0).cast(pl.Int32).rolling_mean(14) / 
             (pl.col("Close").diff().abs().rolling_mean(14) + 1e-9)).alias("RSI_Proxy"),
            
            # Volatility
            pl.col("Close").rolling_std(20).alias("Vol_20"),
            (pl.col("High") - pl.col("Low")).rolling_mean(14).alias("ATR_14"),
            
            # Fundamental Ratios (Fill quarterly gaps with forward-fill)
            (pl.col("Net Income") / pl.col("Total Assets")).alias("ROA"),
            (pl.col("Net Income") / pl.col("Revenue")).alias("Net_Margin"),
        ])

        # 4. Target Engineering
        df_ticker = df_ticker.with_columns([
            pl.col("Log_Return_1d").shift(-1).alias("Target_Log_Return"),
            (pl.col("Close").shift(-1) > pl.col("Close")).cast(pl.Int64).alias("Target_Is_Up")
        ])

        # 5. Final Cleaning per Ticker
        # Drop rows missing SMA_200 (start of history) and Target (end of history)
        df_ticker = df_ticker.drop_nulls(subset=["Dist_SMA_200", "Target_Log_Return"])
        
        # Forward fill fundamentals (ROA, Margin) since they only change quarterly
        df_ticker = df_ticker.with_columns([
            pl.col("ROA").fill_null(strategy="forward"),
            pl.col("Net_Margin").fill_null(strategy="forward"),
        ]).fill_null(0.0) # Fill remaining (start of history fundamentals)

        all_processed.append(df_ticker)

    # 6. Combine all tickers
    final_df = pl.concat(all_processed)
    
    # Add Company Metadata (IndustryId and Number Employees)
    final_df = final_df.join(
        df_meta.select(["Ticker", "IndustryId", "Number Employees"]), 
        on="Ticker", 
        how="left"
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_df.write_parquet(output_path)
    
    print(f"\nETL Complete. Final Feature Set: {final_df.shape}")
    print(f"Stored at: {output_path}")

if __name__ == "__main__":
    process_all_companies()
