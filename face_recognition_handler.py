import cv2
import face_recognition
import os
import numpy as np
from pymongo import MongoClient

class FaceRecognitionHandler:
    def __init__(self, images_path, mongo_uri):
        self.client = MongoClient(mongo_uri)
        self.db = self.client.face_recognition_db
        self.faces_collection = self.db.faces

        self.known_face_encodings, self.known_face_names = self.load_known_faces(images_path)

    def load_known_faces(self, path):
        images = []
        class_names = []
        my_list = os.listdir(path)
        for cl in my_list:
            cur_img = cv2.imread(f'{path}/{cl}')
            images.append(cur_img)
            class_names.append(os.path.splitext(cl)[0])

        encode_list = []
        for img, name in zip(images, class_names):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encode_list.append(encode)
            self.save_face_to_db(name, encode) # saves face encoding to MongoDB

        return encode_list, class_names

    def save_face_to_db(self, name, encoding):
        face_data = {
            "name": name,
            "encoding": encoding.tolist()  # Convert numpy array to list for storage
        }
        self.faces_collection.update_one(
            {"name": name},
            {"$set": face_data},
            upsert=True
        )

    def load_faces_from_db(self):
        faces = self.faces_collection.find()
        encode_list = []
        class_names = []
        for face in faces:
            encode_list.append(np.array(face["encoding"]))
            class_names.append(face["name"])
        return encode_list, class_names

    def get_face_locations(self, img):
        return face_recognition.face_locations(img)

    def get_face_encodings(self, img, face_locations):
        return face_recognition.face_encodings(img, face_locations)

    def identify_face(self, face_encoding):
        self.known_face_encodings, self.known_face_names = self.load_faces_from_db()

        matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            return self.known_face_names[best_match_index].upper()
        return None

    def draw_checkedin_face(self, img, face_location, name):
        y1, x2, y2, x1 = face_location
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 255), cv2.FILLED)
        cv2.putText(img, "Checked In", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    def draw_unknown_face(self, img, face_location):
        y1, x2, y2, x1 = face_location
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, "Unknown Person", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)