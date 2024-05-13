import cv2
import numpy as np
import json

# draw the result of the string art
class StringArtDrawer:
    def __init__(self, input_image, config_file = "Draw_config.json", width=255, height=255):
        self.nails = [] #儲存各個釘子的x,y座標及灰階值，如[(100,200,150)]，第一個釘子的xy座標為(100,200)，其灰階值為150
        self.width = width
        self.height = height
        self.image = self.resize(input_image)
        self.image = self.tocircle(self.image)
        # read config file
        with open(config_file, "r") as f:
            config_file = json.load(f)
            self.num_nails = config_file["num_nails"]
        
    
    def initialize_nails(self): #初始圖中的釘子
        image = self.image
        height, width = image.shape[:2]
        center = (width // 2, height // 2)  
        radius = min(width, height) // 2 - 1
        angles = np.linspace(0, 2 * np.pi, self.num_nails, endpoint=False)

        for angle in angles:
            x = int(center[0] + radius * np.cos(angle))
            y = int(center[1] + radius * np.sin(angle))
            
            x = max(0, min(x, width - 1))
            y = max(0, min(y, height - 1))
            
            gray_value = image[y, x]

            self.nails.append((x, y, gray_value))

    def connect_nails(self, nail1, nail2): #nail1、nail2分別為兩釘子的x,y座標，將兩釘子連接成線
        cv2.line(self.image, nail1, nail2, (0, 0, 0), thickness=1)
        length = np.linalg.norm(np.array(nail2) - np.array(nail1))
        angle = np.arctan2(nail2[1] - nail1[1], nail2[0] - nail1[0])

        delta_x = 0.5 * np.sin(angle + np.pi/2)
        delta_y = 0.5 * np.cos(angle + np.pi/2)
        start1 = (int(nail1[0] + delta_x), int(nail1[1] + delta_y))
        end1 = (int(nail2[0] + delta_x), int(nail2[1] + delta_y))
        start2 = (int(nail1[0] - delta_x), int(nail1[1] - delta_y))
        end2 = (int(nail2[0] - delta_x), int(nail2[1] - delta_y))

        cv2.line(self.image, start1, end1, (0, 0, 0), thickness=1)
        cv2.line(self.image, start2, end2, (0, 0, 0), thickness=1)

    def resize(self, image):
        return cv2.resize(image, (self.width, self.height), interpolation=cv2.INTER_AREA)

    def tocircle(self, input_image):
        height, width = input_image.shape
        radius = width // 2
        output_image = np.zeros((height, width), dtype=np.uint8) #創建一個空白的圓形圖片

        cv2.circle(output_image, (width // 2, height // 2), radius, (255, 255, 255), -1)
        output_image = cv2.bitwise_and(input_image, output_image)
        # output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2GRAY) #轉灰階圖
        return output_image

    # decode the population to np.ndarray
    def Decode(self, population):
        pass
