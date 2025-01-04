# externalapi/api_client.py

import requests
from .config import BASE_URL, AUTHORIZATION_TOKEN

class ExternalAPIClient:
    @staticmethod
    def make_request(endpoint, method='GET', headers=None, data=None):
        url = f"{BASE_URL}/{endpoint}"
        default_headers = {
            "Authorization": AUTHORIZATION_TOKEN,
            "Content-Type": "application/json",
        }
        if headers:
            default_headers.update(headers)

        try:
            if method == 'POST':
                response = requests.post(url, headers=default_headers, json=data)
            elif method == 'GET':
                response = requests.get(url, headers=default_headers, params=data)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
