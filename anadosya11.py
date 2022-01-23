import cv2
from gui_buttons import Buttons

# Initialize Buttons
button = Buttons()
button.add_button("insan", 20, 20)
button.add_button("cep telefonu", 20, 100)
button.add_button("keyboard", 20, 180)
button.add_button("uzaktan kumanda", 20, 260)
button.add_button("makas", 20, 340)



# Opencv DNN
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320, 320), scale=1/255)


# Load class lists
classes = []
with open("dnn_model/classes.txt", "r") as file_object:
    for class_name in file_object.readlines():

        class_name = class_name.strip()  # satır arası boşluklar için
        classes.append(class_name)



# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # webcam görüntü penceresini büyütmek için
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# FULL HD 1920 x 1080


def click_button(event, x, y, flags, params):
    global buton_insan
    if event == cv2.EVENT_LBUTTONDOWN:
        button.button_click(x, y)


# Frame isimli pencerede fareye tıklandığında click_button isimli metod çağırılacak
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_button)


while True:
    # Get frames
    ret, frame = cap.read()

    # Get active buttons list
    active_buttons = button.active_buttons_list()
    #print("Active buttons", active_buttons)


    # Object Detection
    (class_ids, scores, bboxes) = model.detect(frame, confThreshold=0.3, nmsThreshold=.4)
    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        (x, y, w, h) = bbox


        class_name = classes[class_id]

        if class_name in active_buttons:
            cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 3, (200,0,50), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 0, 50), 3)


    # Display buttons
    button.display_buttons(frame)


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

