import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY = os.getenv("SIMFIN_API_KEY")

def debug_tickers():
    tickers = ["GOOGL", "META", "AAPL"] # AAPL as control
    url = "https://backend.simfin.com/api/v3/companies/prices/compact"
    headers = {"Authorization": API_KEY}
    
    for ticker in tickers:
        print(f"\n--- Testing Ticker: {ticker} ---")
        r = requests.get(url, params={"ticker": ticker}, headers=headers)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            if not data:
                print(f"Result: EMPTY LIST for {ticker}")
            else:
                item = data[0]
                print(f"Result: Success. Rows returned: {len(item.get('data', []))}")
                print(f"Columns: {item.get('columns')}")
        else:
            print(f"Result: Error - {r.text}")

if __name__ == "__main__":
    debug_tickers()
