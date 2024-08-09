import requests
import json

class OLEDDisplay:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def send_data(self, data):
        url = f"http://{self.ip_address}/update"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print("Data sent successfully to OLED")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")