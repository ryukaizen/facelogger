import cv2
import numpy as np
from esp32_camera import ESP32Camera
from face_recognition_handler import FaceRecognitionHandler
from checkin_manager import CheckinManager
from oled_display import OLEDDisplay

ESP32_CAM_URL = 'http://192.168.52.160/640x480.jpg' # replace this with your own ESP32-CAM generated link, check aithinker folder
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz/formResponse" # replace this with your own Google Form URL
MONGODB_URL = 'mongodb://localhost:27017/'  # replace this with your own MongoDB URL

# Inspect element on the Google Form and find the entry name ID and entry time ID
ENTRY_NAME_ID = 'entry.123456789' 
ENTRY_TIME_ID = 'entry.987654321'


def main():
    esp32_cam = ESP32Camera(ESP32_CAM_URL)
    face_handler = FaceRecognitionHandler('training_data', MONGODB_URL)
    checkin_manager = CheckinManager(GOOGLE_FORM_URL, ENTRY_NAME_ID, ENTRY_TIME_ID)
    oled_display = OLEDDisplay('192.168.52.160')  # add the IP address from ESP32-CAM generated link

    while True:
        img = esp32_cam.get_image()
        if img is not None:
            img_s = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB)

            face_locations = face_handler.get_face_locations(img_s)
            face_encodings = face_handler.get_face_encodings(img_s, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                name = face_handler.identify_face(face_encoding)
                if name:
                    checkin_manager.mark_checkin(name)
                    checkin_manager.mark_checkin_csv(name)
                    oled_display.send_data(f"Checked In\n{name}")
                    face_handler.draw_checkedin_face(img, face_location, name)
                else:
                    oled_display.send_data("Unknown\nperson!")
                    face_handler.draw_unknown_face(img, face_location)

            cv2.imshow('ESP32-CAM', img)
            cv2.waitKey(1)

if __name__ == "__main__":
    main()