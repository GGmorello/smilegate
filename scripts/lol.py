import cv2

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_classifier = cv2.CascadeClassifier('haarcascade_smile.xml')
eye_classifier = cv2.CascadeClassifier('haarcascade_eye.xml')

def detect(gray, frame):
    det_faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    for (fx, fy, fw, fh) in det_faces:
        cv2.rectangle(frame, (fx, fy), ((fx + fw), (fy + fh)), (255, 0, 0), 2)

        region_of_interest_gray = gray[fy:fy + fh, fx:fx + fw]
        region_of_interest_color = frame[fy:fy + fh, fx:fx + fw]

        det_smiles = smile_classifier.detectMultiScale(region_of_interest_gray, 1.7, 22)
        for (sx, sy, sw, sh) in det_smiles:
            cv2.rectangle(region_of_interest_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)

        det_eyes = eye_classifier.detectMultiScale(region_of_interest_gray, 1.1, 22)
        for (ex, ey, ew, eh) in det_eyes:
            cv2.rectangle(region_of_interest_color, (ex, ey), ((ex + ew), (ey + eh)), (0, 255, 0), 2)

    return frame

video_capture = cv2.VideoCapture(0)

while True:
    _, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    canvas = detect(gray, frame)

    cv2.imshow('Video', canvas)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
