import cv2
import numpy as np


# draw the result of the string art
class StringArtDrawer:
    def __init__(self):
        self.nails = [] #儲存各個釘子的x,y座標及灰階值，如[(100,200,150)]，第一個釘子的xy座標為(100,200)，其灰階值為150

    def initialize_nails(self): #初始圖中的釘子
        pass

    def connect_nails(self, nail1, nail2): #nail1、nail2分別為兩釘子的x,y座標，將兩釘子連接成線
        pass
