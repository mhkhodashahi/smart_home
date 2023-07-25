import face_recognition
import numpy as np


class recognition:

    unknown_face = 'Unknown'

    def __init__(self):
        self.known_face_encodings = list()
        self._loadImages()

    def _loadImages(self):
        image = face_recognition.load_image_file("./recognition/images/mh.png")

        self.known_face_encodings.append( face_recognition.face_encodings(image)[0])
        image = face_recognition.load_image_file("./recognition/images/fa.jpeg")
        self.known_face_encodings.append( face_recognition.face_encodings(image)[0])
        # Create arrays of known face encodings and their names

        self.known_face_names = [
            "Mohammad",
            "Fatemeh"
        ]

    def label_face_name(self, small_frame):
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = self.unknown_face

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            face_names.append(name)
        return face_names, face_locations
