from pypylon import pylon
import cv2
import time

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


# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()

camera.ExposureTime = 105000

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

starting_time = time.time()
kare_id = 0
font = cv2.FONT_HERSHEY_PLAIN

while camera.IsGrabbing():
    kare_id += 1
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        cv2.namedWindow('title', cv2.WINDOW_NORMAL)

        # Object Detection
        (class_ids, scores, bboxes) = model.detect(img, confThreshold=0.3, nmsThreshold=.4)
        for class_id, score, bbox in zip(class_ids, scores, bboxes):
            (x, y, w, h) = bbox
            cv2.rectangle(img, (x, y), (x + w, y + h), (200, 0, 50), 3)

            class_name = classes[class_id]

            cv2.putText(img, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 3, (200, 0, 50), 2)


        elapsed_time = time.time() - starting_time
        fps = kare_id / elapsed_time
        cv2.putText(img, "FPS: " + str(round(fps, 2)), (10, 50), font, 4, (0, 0, 0), 3)

        cv2.imshow('title', img)
        k = cv2.waitKey(1)
        if k == 27:
            break
    grabResult.Release()

# Releasing the resource
camera.StopGrabbing()

cv2.destroyAllWindows()
