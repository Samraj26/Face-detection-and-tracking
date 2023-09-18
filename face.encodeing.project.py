import pickle
import cv2
import face_recognition
import numpy as np
import time
from cvzone.SerialModule import SerialObject

with open('encodes', 'rb') as f:
    classNames,encodeListKnown = pickle.load(f)

cap = cv2.VideoCapture(0)
arduino = SerialObject("/dev/cu.usbmodem14101")

faceFound = False

while True:
    success , img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            print("Face Found")
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4,x2 * 4, y2 * 4,x1 * 4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_PLAIN, 1.5, (255,255,255), 3)
            if faceFound is not True:
                print("Door Opened")
                arduino.sendData([1])
                startTime = time.time()
                faceFound = True

    if faceFound:
         totalTime = time.time()-startTime
         print(totalTime)
         if totalTime>5:
              print("Door Closed")
              arduino.sendData([0])
              faceFound = False


    cv2.imshow("image",img)
    cv2.waitKey(1)

