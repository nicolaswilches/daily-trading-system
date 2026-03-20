import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY = os.getenv("SIMFIN_API_KEY")

def test_new_auth():
    print(f"API Key: {API_KEY[:3]}...")

    # 1. Test v1 with Direct Key (Doc suggestion)
    print("\nTest 1: v1 with Direct Key header")
    url_v1 = "https://backend.simfin.com/api/v1/info/share-prices"
    r1 = requests.get(url_v1, params={"ticker": "AAPL", "start": "2025-01-01"}, headers={"Authorization": API_KEY})
    print(f"v1 Status: {r1.status_code}")

    # 2. Test v3 with Direct Key (Doc suggestion)
    print("\nTest 2: v3 with Direct Key header")
    url_v3 = "https://backend.simfin.com/api/v3/companies/prices/compact"
    r2 = requests.get(url_v3, params={"ticker": "AAPL"}, headers={"Authorization": API_KEY})
    print(f"v3 Status: {r2.status_code}")
    if r2.status_code == 200:
        print("✅ SUCCESS with V3!")
        print(r2.json()[:1])

if __name__ == "__main__":
    test_new_auth()
