import cv2
from cvzone.FaceDetectionModule import FaceDetector
from cvzone .PIDModule import PID
from cvzone.PlotModule import LivePlot
from cvzone.SerialModule import SerialObject

cap = cv2.VideoCapture(1)

detector = FaceDetector(minDetectionCon=0.75)
arduino = SerialObject("/dev/cu.usbmodem14101",digits=3)


xPID = PID([0.04, 0, 0.02], 640 // 2, axis=0)
yPID = PID([0.04, 0, 0.02], 200, axis=1)
xPlot = LivePlot(yLimit=[0, 640], char="X")
yPlot = LivePlot(yLimit=[0, 400], char="Y")
xAngle , yAngle = 90, 0


while True:
    success, img = cap.read()
    img, bboxs = detector.findFaces(img)


    if bboxs:
        x, y, w, h = bboxs[0]['bbox']
        cx, cy = bboxs[0]['center']
        resultX = int(xPID.update(cx))
        resultY = int(yPID.update(cy))
        xAngle -= resultX
        yAngle += resultY
        print(resultX)
        imgPlotX = xPlot.update(cx)
        imgPlotY = yPlot.update(cy)


        img = xPID.draw(img, [cx, cy])
        img = yPID.draw(img, [cx, cy])
        cv2.imshow("Image PLOT X ", imgPlotX)
        cv2.imshow("Image PLOT Y ", imgPlotY)



    arduino.sendData([xAngle, yAngle])

    cv2.imshow("Image", img)
    cv2.waitKey(1)