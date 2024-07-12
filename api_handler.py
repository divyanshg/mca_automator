import requests
from config import API_URL
from encryption import encrypt

def fetch_company_data(cin):
    encrypted_data = encrypt(f"ID={cin}&requestID=cin")
    headers = {
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "DNT": "1",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://www.mca.gov.in/content/mca/global/en/mca/master-data/MDS.html",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-platform": '"macOS"'
    }
    
    try:
        response = requests.request("POST", API_URL, headers=headers, data=f"data={encrypted_data}")

        # Raise HTTPError for bad responses
        response.raise_for_status()

        # Check if response is successful
        if response.status_code == 200:
            try:
                json_response = response.json()
                company_data = json_response.get('data', {}).get('companyData', {})
                return company_data
            except ValueError as e:
                print(f"Error decoding JSON: {e}")
                print(f"Response content: {response.text}")
                return None
        else:
            print(f"Unexpected status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
