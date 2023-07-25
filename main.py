import cv2
import time
import datetime
from smart_home.recognition.recognition import recognition

capture_id = 0
cap = cv2.VideoCapture(capture_id)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")
b_body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_upperbody.xml")
frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

out = None
detection = False
detection_stopped_time = None
timer_started = False
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
reco = recognition()

while True:
    _, frame = cap.read()

    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except Exception as err:
        continue
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            face_names, face_locations = reco.label_face_name(small_frame)
        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        if detection:
            timer_started = False
        elif all(value == reco.unknown_face for value in face_names) and len(face_names) > 0:
            print(face_names)
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter("./videos/" + current_time + ".mp4", fourcc, 20, frame_size)
            print("Started recording")
        if not all(value == reco.unknown_face for value in face_names):
            if out is not None:
                detection = False
                out.release()
                out = None
                print(face_names)
                print('stop recording')
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= 5:
                detection = False
                timer_started = False
                out.release()
                print('stop recording')
        else:
            timer_started = True
            detection_stopped_time = time.time()
    r = 800.0 / frame.shape[1]
    dim = (800, int(frame.shape[0] * r))

    # perform the actual resizing of the image
    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite(f'./images/frame_{capture_id}.jpg', resized)
    if len(face_names) > 0:
        cv2.imwrite("./images/frame_name.jpg", frame)
    if (detection):
        out.write(frame)
    cv2.imshow("camera", frame)
    if cv2.waitKey(1) == ord('q'):
        if out is not None:
            out.release()
        break

cap.release()
