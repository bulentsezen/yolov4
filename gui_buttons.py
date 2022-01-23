import cv2
import numpy as np


class Buttons:
    def __init__(self):
        # Font
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.text_scale = 3
        self.text_thick = 3
        self.x_margin = 20
        self.y_margin = 10

        # Buttons
        self.buttons = {}
        self.button_index = 0
        self.buttons_area = []

        np.random.seed(0)
        self.colors = []
        self.generate_random_colors()

    def generate_random_colors(self):
        for i in range(91):
            random_c = np.random.randint(256, size=3)
            self.colors.append((int(random_c[0]), int(random_c[1]), int(random_c[2])))


    def add_button(self, text, x, y):
        # Get text size
        textsize = cv2.getTextSize(text, self.font, self.text_scale, self.text_thick)[0]
        right_x = x + (self.x_margin * 2) + textsize[0]
        bottom_y = y + (self.y_margin * 2) + textsize[1]

        self.buttons[self.button_index] = {"text": text, "position": [x, y, right_x, bottom_y], "active": False}
        self.button_index += 1

    def display_buttons(self, frame):
        for b_index, button_value in self.buttons.items():
            button_text = button_value["text"]
            (x, y, right_x, bottom_y) = button_value["position"]
            active = button_value["active"]

            if active:
                button_color = (0, 0, 200)
                text_color = (255, 255, 255)
                thickness = -1
            else:
                button_color = (0, 0, 200)
                text_color = (0, 0, 200)
                thickness = 3

            # Get  text size
            cv2.rectangle(frame, (x, y), (right_x, bottom_y),
                          button_color, thickness)
            cv2.putText(frame, button_text, (x + self.x_margin, bottom_y - self.y_margin),
                        self.font, self.text_scale, text_color, self.text_thick)
        return frame


    def button_click(self, mouse_x, mouse_y):
        for b_index, button_value in self.buttons.items():
            (x, y, right_x, bottom_y) = button_value["position"]
            active = button_value["active"]
            area = [(x, y), (right_x, y), (right_x, bottom_y), (x, bottom_y)]

            inside = cv2.pointPolygonTest(np.array(area, np.int32), (int(mouse_x), int(mouse_y)), False)
            if inside > 0:
                print("IS Ac", active)
                new_status = False if active is True else True
                self.buttons[b_index]["active"] = new_status

    def active_buttons_list(self):
        active_list = []
        for b_index, button_value in self.buttons.items():
            active = button_value["active"]
            text = button_value["text"]
            if active:
                active_list.append(str(text).lower())

        return active_list




