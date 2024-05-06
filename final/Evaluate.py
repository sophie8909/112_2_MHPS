import numpy as np
import cv2
class Evaluate:
    def __init__(self, original_img, mode="DHash"):
        self.original_img = original_img
        self.mode = mode
    
    def __call__(self, result_img, kernel_size=3):
        if self.original_img.shape != result_img.shape:
            result_img = cv2.resize(result_img, (self.original_img.shape[1], self.original_img.shape[0]))
        if self.mode == "1-pixel":
            return self.one_pixel_diff(result_img)
        elif self.mode == "convolution":
            return self.convolution_diff(result_img, kernel_size)
        elif self.mode == "DHash":
            return self.DHash(result_img)
        else:
            print("Invalid mode in Evaluate")

    def one_pixel_diff(self, result_img):
        # calculate the difference between the original image and the result image
        diff = np.sum(np.abs(self.original_img - result_img))
        print(diff)
        return diff

    def convolution_diff(self, result_img, kernel_size=3):
        # calculate the difference between the original image and the result image using convolution
                
        kernel = np.ones((kernel_size, kernel_size), dtype=np.float32) / kernel_size**2

        #進行convolute，
        result = cv2.filter2D(result_img, -1, kernel)
        original = cv2.filter2D(self.original_img, -1, kernel)
        diff = np.sum(np.abs(original - result))
        print(diff)
        return diff
    
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
        print(diff)
