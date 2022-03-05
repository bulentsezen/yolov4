import cv2
import os
from pygame import mixer  # Load the pygame library
import time
from gtts import gTTS

def seslendir(class_name):
    metin = "Bir " + class_name + " algılandı."
    tts = gTTS(metin, lang="tr")
    dosya_adi = str(class_name)+'.mp3'
    tts.save(dosya_adi)

    mixer.init()
    mixer.music.load(dosya_adi)
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(0.1)


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
cap = cv2.VideoCapture(0)

insan_algilandi = False
cep_telefonu_algilandi = False

while True:
    # Get frames
    ret, frame = cap.read()

    # Object Detection
    (class_ids, scores, bboxes) = model.detect(frame, confThreshold=0.3, nmsThreshold=.4)
    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        (x, y, w, h) = bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), (200,0,50), 3)

        class_name = classes[class_id]

        cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 3, (200,0,50), 2)

        if not insan_algilandi and class_name == "insan":
            seslendir(class_name)
            insan_algilandi = True


        if not cep_telefonu_algilandi and class_name == "cep telefonu":
            seslendir(class_name)
            cep_telefonu_algilandi = True


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

