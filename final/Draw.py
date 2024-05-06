import cv2
import numpy as np


# draw the result of the string art
class StringArtDrawer:
    def __init__(self, input_image):
        self.nails = [] #儲存各個釘子的x,y座標及灰階值，如[(100,200,150)]，第一個釘子的xy座標為(100,200)，其灰階值為150
        self.image = self.tocircle(input_image)
        self.num_nails = 288 #先寫在這，之後要放參數檔中
    
    def initialize_nails(self, image): #初始圖中的釘子
        _, thresholded = cv2.threshold(image, 240, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        circle_contour = contours[0]  # 假設只有一個圓形
        points = np.linspace(0, 2*np.pi, self.num_nails, endpoint=False)

        for i in range(self.nums_nails):
            angle = points[i]
            x = int(circle_contour[0][0][0] + 0.9 * np.cos(angle))
            y = int(circle_contour[0][0][0] + 0.9 * np.sin(angle))

            gray_value = image[y, x]
            self.nails.append((x, y, gray_value))

    def connect_nails(self, nail1, nail2): #nail1、nail2分別為兩釘子的x,y座標，將兩釘子連接成線
        pass

    def tocircle(self, input_image):
        height, width = input_image.shape
        radius = width // 2
        output_image = np.zeros((height, width, 3), dtype=np.uint8) #創建一個空白的圓形圖片
        cv2.circle(output_image, (width // 2, height // 2), radius, (255, 255, 255), -1)
        output_image = cv2.bitwise_and(input_image, output_image)
        output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2GRAY) #轉灰階圖
        return output_image
