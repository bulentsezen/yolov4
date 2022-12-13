import cv2
import os
import time
import pypylon.pylon as py

icam = py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())
icam.Open()
icam.PixelFormat = "RGB8"
cv2.namedWindow("1",cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
cv2.resizeWindow("1", 600,600)

# Opencv DNN
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320, 320), scale=1/255)


# Load class lists
classes = []
with open("dnn_model/classes.txt", "r") as file_object:
    for class_name in file_object.readlines():

        class_name = class_name.strip()  # satır arası boşluklar için
        print(class_name)
        classes.append(class_name)


# Initialize camera
#cap = cv2.VideoCapture(0)

ses = False

starting_time = time.time()
frame_id = 0
font = cv2.FONT_HERSHEY_PLAIN

while True:
    # Get frames
    # ret, frame = cap.read()

    img = icam.GrabOne(4000)
    img = img.Array
    frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    frame_id += 1

    # Object Detection
    (class_ids, scores, bboxes) = model.detect(frame, confThreshold=0.3, nmsThreshold=.4)
    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        (x, y, w, h) = bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), (200,0,50), 3)

        class_name = classes[class_id]

        cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 3, (200,0,50), 2)

        if not ses:
            metin = "Bir "+ class_name + " algılandı."
            print(metin)
            ses = True

    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 4, (0, 0, 0), 3)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

