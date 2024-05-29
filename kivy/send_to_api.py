import requests
from requests.exceptions import ConnectionError

def send_data_to_api(uuid, hash_value, api_url):
        # Data to be sent to API
        data = {
            'uuid': uuid,
            'hash_value': hash_value
        }
        try:
        # Sending post request to the API endpoint
            response = requests.post(api_url, json=data)

            return response
        except ConnectionError:
              return 'Failed to establish a new connection'
            
        #     return response.json()  # Assuming the response contains JSON data
        # else:
        #     print(f"Failed to send data to API. Status code: {response.status_code}, Response: {response.text}")
        #     return None