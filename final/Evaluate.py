import numpy as np
import cv2
from Draw import StringArtDrawer
class Evaluate:
    def __init__(self, original_img, mode="DHash"):
        self.original_img = original_img
        self.mode = mode
    
    def __call__(self, population: set):
        # try:
            result_img = StringArtDrawer(self.original_img)
            result_img.Decode(population)
            return self.__evaluate(result_img.image)
        # except Exception as e:
        #     print(e)
        #     return -1


    def __evaluate(self, result_img: np.ndarray):
        return self.DHash(result_img)

    def __dhash(self, img):
        # calculate the difference hash of the image
        img = cv2.resize(img, (33, 32))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        diff = img[:, 1:] > img[:, :-1]
        return diff.flatten()

    def DHash(self, result_img):
        original_hash = self.__dhash(self.original_img)
        # print(original_hash)
        result_hash = self.__dhash(result_img)
        # print(result_hash)
        diff = np.sum(original_hash != result_hash)
        return diff
