import cv2
import numpy as np


# draw the result of the string art
class StringArtDrawer:
    def __init__(self, input_image):
        self.nails = [] #儲存各個釘子的x,y座標及灰階值，如[(100,200,150)]，第一個釘子的xy座標為(100,200)，其灰階值為150
        self.image = self.tocircle(input_image)
        
    def initialize_nails(self): #初始圖中的釘子
        pass

    def connect_nails(self, nail1, nail2): #nail1、nail2分別為兩釘子的x,y座標，將兩釘子連接成線
        pass

    def tocircle(self, input_image):
        height, width = input_image.shape
        radius = width // 2
        output_image = np.zeros((height, width, 3), dtype=np.uint8) #創建一個空白的圓形圖片
        cv2.circle(output_image, (width // 2, height // 2), radius, (255, 255, 255), -1)
        output_image = cv2.bitwise_and(input_image, output_image)
        return output_image
