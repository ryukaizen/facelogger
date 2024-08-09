import requests
import numpy as np
import cv2

class ESP32Camera:
    def __init__(self, url):
        self.url = url

    def get_image(self):
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                img_array = np.array(bytearray(response.content), dtype=np.uint8)
                img = cv2.imdecode(img_array, -1)
                return img
        except Exception as e:
            print(f"Error fetching image from ESP32-CAM: {str(e)}")
        return None