import requests

def fetch_page(url):
    try:
        print(f"Fetching {url}")
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return None

