import requests

BASE_URL = "http://10.74.216.125:5000/api"

def test_search():
    url = f"{BASE_URL}/search"
    payload = {"query": "chicken", "type": "recipe"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        print("🔎 /search")
        print("Status:", r.status_code)
        print("Response:", r.json() if r.headers.get("Content-Type") == "application/json" else r.text)
    except Exception as e:
        print("❌ /search failed:", str(e))

def test_health():
    url = f"{BASE_URL}/health"
    try:
        r = requests.get(url, timeout=10)
        print("💚 /health")
        print("Status:", r.status_code)
        print("Response:", r.json() if r.headers.get("Content-Type") == "application/json" else r.text)
    except Exception as e:
        print("❌ /health failed:", str(e))

def test_root():
    url = f"{BASE_URL}/"
    try:
        r = requests.get(url, timeout=10)
        print("🏠 /")
        print("Status:", r.status_code)
        print("Response:", r.text)
    except Exception as e:
        print("❌ / failed:", str(e))

if __name__ == "__main__":
    test_health()
    test_root()
    test_search()
