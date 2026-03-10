import os
import requests
import polars as pl
from dotenv import load_dotenv
import time

# Load API key
load_dotenv()
API_KEY = os.getenv("SIMFIN_API_KEY")
BASE_URL = "https://backend.simfin.com/api/v1"

# Tickers to fetch
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META"]

def fetch_prices(ticker):
    """Fetch daily share prices for a given ticker."""
    print(f"Fetching prices for {ticker}...")
    url = f"{BASE_URL}/info/share-prices"
    params = {
        "ticker": ticker,
        "start": "2019-01-01",
        "end": "2025-01-01"
    }
    headers = {
        "Authorization": f"api-key {API_KEY}"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Check if the response contains the expected data
        if not data or "data" not in data:
            print(f"No data found for {ticker}")
            return None
            
        columns = data["columns"]
        rows = data["data"]
        
        df = pl.DataFrame(rows, schema=columns, orient="row")
        df = df.with_columns(pl.lit(ticker).alias("Ticker"))
        return df
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

def main():
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        print("Please set your SIMFIN_API_KEY in the .env file.")
        return

    all_data = []
    for ticker in TICKERS:
        df = fetch_prices(ticker)
        if df is not None:
            all_data.append(df)
        # Respect rate limits (max 2 requests per second)
        time.sleep(1) 
    
    if all_data:
        final_df = pl.concat(all_data)
        os.makedirs("data/raw", exist_ok=True)
        final_df.write_parquet("data/raw/prices.parquet")
        print(f"Saved {len(final_df)} rows to data/raw/prices.parquet")
    else:
        print("No data fetched.")

if __name__ == "__main__":
    main()
