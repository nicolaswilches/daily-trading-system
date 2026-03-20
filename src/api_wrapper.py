import os
import requests
import polars as pl
import time
from dotenv import load_dotenv

class PySimFin:
    """
    A professional wrapper for the SimFin API v3 with built-in rate-limiting 
    and data formatting for Polars.
    """
    # Updated to V3
    BASE_URL = "https://backend.simfin.com/api/v3"

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("SIMFIN_API_KEY")
        if not self.api_key:
            raise ValueError("SIMFIN_API_KEY not found in .env file.")
        
        # Documentation format: Direct key in Authorization header
        self.headers = {
            "Authorization": self.api_key
        }
        self.last_call_time = 0

    def _rate_limit(self):
        """Ensures we don't exceed 2 requests per second."""
        elapsed = time.time() - self.last_call_time
        if elapsed < 0.6:  # 0.6s delay for safety
            time.sleep(0.6 - elapsed)
        self.last_call_time = time.time()

    def get_share_prices(self, ticker):
        """
        Fetches daily share prices for a specific ticker (V3 Compact).
        """
        self._rate_limit()
        print(f"API: Fetching live prices for {ticker} (V3)...")
        
        url = f"{self.BASE_URL}/companies/prices/compact"
        params = {"ticker": ticker}
        
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        json_data = response.json()
        
        if not json_data or len(json_data) == 0:
            return None
            
        # V3 Compact returns a list of objects, usually one per ticker
        item = json_data[0]
        df = pl.DataFrame(item["data"], schema=item["columns"], orient="row")
        
        # Map V3 column names to our expected ETL names
        # V3: 'Last Closing Price' -> ETL expectation: 'Close'
        rename_map = {
            "Date": "Date",
            "Opening Price": "Open",
            "Highest Price": "High",
            "Lowest Price": "Low",
            "Last Closing Price": "Close",
            "Trading Volume": "Volume",
            "Dividend Paid": "Dividend"
        }
        
        # Only rename columns that exist in the V3 response
        current_cols = df.columns
        actual_rename = {k: v for k, v in rename_map.items() if k in current_cols}
        
        df = df.rename(actual_rename)
        df = df.with_columns(pl.lit(ticker).alias("Ticker"))
        
        return df

    def get_fundamentals(self, ticker, statement="income"):
        """Fetches the latest quarterly fundamental statements (V3)."""
        self._rate_limit()
        print(f"API: Fetching {statement} for {ticker} (V3)...")
        
        # V3 statement endpoint
        url = f"{self.BASE_URL}/companies/statements/compact"
        params = {
            "ticker": ticker,
            "stype": "pl" if statement == "income" else "bs", # pl = Profit/Loss, bs = Balance Sheet
            "period": "qu"
        }
        
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        json_data = response.json()
        
        if not json_data or len(json_data) == 0:
            return None
            
        item = json_data[0]
        return pl.DataFrame(item["data"], schema=item["columns"], orient="row")

if __name__ == "__main__":
    api = PySimFin()
    try:
        df = api.get_share_prices("AAPL")
        print(df.tail())
    except Exception as e:
        print(f"Test Failed: {e}")
