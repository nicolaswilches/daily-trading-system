import os
import simfin as sf
import polars as pl
import pandas as pd
from dotenv import load_dotenv

# --- MONKEYPATCH FOR SIMFIN/PANDAS COMPATIBILITY ---
# Newer pandas deprecated 'date_parser' in favor of 'date_format' or 'parse_dates'
# We temporarily wrap read_csv to handle the old argument used by simfin
original_read_csv = pd.read_csv
def patched_read_csv(*args, **kwargs):
    if 'date_parser' in kwargs:
        kwargs.pop('date_parser')
        kwargs['parse_dates'] = True 
    return original_read_csv(*args, **kwargs)
pd.read_csv = patched_read_csv
# ----------------------------------------------------

load_dotenv()
API_KEY = os.getenv("SIMFIN_API_KEY")
TICKERS = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META"]

def main():
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        print("Please set your SIMFIN_API_KEY in the .env file.")
        return

    sf.set_api_key(API_KEY)
    sf.set_data_dir("data/raw")
    
    print("Fetching bulk US data (Prices, Companies, Fundamentals)...")
    
    try:
        # These functions will now use our patched read_csv
        sf.load_shareprices(variant='daily', market='us')
        sf.load_companies(market='us')
        sf.load_income(variant='quarterly', market='us')
        sf.load_balance(variant='quarterly', market='us')
    except Exception as e:
        print(f"Error during sf.load calls: {e}")

    def process_csv(filename, output_name, sep=";"):
        path = f"data/raw/{filename}"
        if os.path.exists(path):
            print(f"Filtering {filename}...")
            # We use ignore_errors because some SimFin CSVs have trailing delimiters
            df = pl.read_csv(path, separator=sep, try_parse_dates=True, ignore_errors=True)
            ticker_col = "Ticker" if "Ticker" in df.columns else "Ticker Symbol"
            df_filtered = df.filter(pl.col(ticker_col).is_in(TICKERS))
            df_filtered.write_parquet(f"data/raw/{output_name}.parquet")
            print(f"Saved {output_name}.parquet")
        else:
            print(f"Error: {filename} not found.")

    process_csv("us-shareprices-daily.csv", "prices")
    process_csv("us-companies.csv", "companies")
    process_csv("us-income-quarterly.csv", "income")
    process_csv("us-balance-quarterly.csv", "balance")

if __name__ == "__main__":
    main()
