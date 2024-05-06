import cv2
import numpy as np


# draw the result of the string art
class StringArtDrawer:
    def __init__(self):
        self.nails = [] #儲存各個釘子的x,y座標及灰階值，如[(100,200,150)]，第一個釘子的xy座標為(100,200)，其灰階值為150

    def init_nails_positions(self):
        pass
