import cv2
import numpy as np
import json
# draw the result of the string art
class StringArtDrawer:
    def __init__(self, input_image, config_file = "config.json"):
        with open(config_file, "r") as f:
            global PARAMETERS
            PARAMETERS = json.load(f)

        self.nails = [] #儲存各個釘子的x,y座標及灰階值，如[(100,200,150)]，第一個釘子的xy座標為(100,200)，其灰階值為150
        self.ori_image = self.resize(input_image)
        self.ori_image = self.tocircle(self.ori_image)

        
        # read config file
        self.initialize_nails()
        
    
    def initialize_nails(self): #初始圖中的釘子
        image = self.ori_image
        height, width = image.shape[:2]
        center = (width // 2, height // 2)  
        radius = min(width, height) // 2 - 1
        angles = np.linspace(0, 2 * np.pi, PARAMETERS["num_nails"], endpoint=False)

        for angle in angles:
            x = int(center[0] + radius * np.cos(angle))
            y = int(center[1] + radius * np.sin(angle))
            
            x = max(0, min(x, width - 1))
            y = max(0, min(y, height - 1))
            
            gray_value = image[y, x]

            self.nails.append((x, y, gray_value))

    def connect_nails(self, img, nail1, nail2, color, thickness): #nail1、nail2分別為兩釘子的x,y座標，將兩釘子連接成線
        nail1 = self.nails[nail1][:2]
        nail2 = self.nails[nail2][:2]
        cv2.line(img, nail1, nail2, color, thickness=thickness)
        
    def resize(self, image):
        return cv2.resize(image, (PARAMETERS["image_size"], PARAMETERS["image_size"]), interpolation=cv2.INTER_AREA)

    def tocircle(self, input_image):
        height, width = input_image.shape
        radius = width // 2
        output_image = np.zeros((height, width), dtype=np.uint8) #創建一個空白的圓形圖片
        output_image += 255

        cv2.circle(output_image, (width // 2, height // 2), radius, (255, 255, 255), -1)
        output_image = cv2.bitwise_and(input_image, output_image)
        # output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2GRAY) #轉灰階圖
        return output_image

    # decode the population to np.ndarray
    def Decode(self, population):
        self.draw_image = np.zeros((PARAMETERS["image_size"], PARAMETERS["image_size"]), dtype=np.uint8)
        self.draw_image += 255
        for (nail1, nail2) in population:
            self.connect_nails(self.draw_image, nail1, nail2,  (0, 0, 0), PARAMETERS["line_width"])

    def Erase_ev(self, population):
        for (nail1, nail2) in population:
            self.connect_nails(self.ori_image, nail1, nail2, (255, 255, 255), PARAMETERS["line_width_ev"])    