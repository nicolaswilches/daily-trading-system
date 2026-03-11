import os
import simfin as sf
import polars as pl
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("SIMFIN_API_KEY")

# Tickers to fetch
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META"]

def main():
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        print("Please set your SIMFIN_API_KEY in the .env file.")
        return

    # Set up simfin
    sf.set_api_key(API_KEY)
    sf.set_data_dir("data/raw")
    
    print("Fetching/Updating bulk US share prices (daily)...")
    csv_path = "data/raw/us-shareprices-daily.csv"
    
    try:
        # This will download the zip and extract the CSV if not present
        # We ignore the return value because it might fail on older pandas
        sf.load_shareprices(variant='daily', market='us')
    except Exception as e:
        print(f"Note: sf.load_shareprices encountered an error during CSV loading, but data may be on disk: {e}")

    if os.path.exists(csv_path):
        print(f"Loading {csv_path} with Polars...")
        # SimFin CSVs use semicolon (;) as separator
        df = pl.read_csv(csv_path, separator=";", try_parse_dates=True)
        
        # Filter for our tickers
        df_filtered = df.filter(pl.col("Ticker").is_in(TICKERS))
        
        # Save to parquet for our ETL pipeline
        output_path = "data/raw/prices.parquet"
        df_filtered.write_parquet(output_path)
        
        print(f"Successfully saved {len(df_filtered)} rows to {output_path}")
        if len(df_filtered) > 0:
            print(f"Date range: {df_filtered['Date'].min()} to {df_filtered['Date'].max()}")
    else:
        print(f"Error: CSV file not found at {csv_path}")

if __name__ == "__main__":
    main()
