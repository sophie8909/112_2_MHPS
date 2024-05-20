import numpy as np
import cv2
from Draw import StringArtDrawer
import json



class Evaluate:
    def __init__(self, original_img, config_file = "config.json"):
        with open(config_file, "r") as f:
            global PARAMETERS
            PARAMETERS = json.load(f)

        self.original_img = original_img
        self.original_img = cv2.resize(self.original_img, (PARAMETERS["image_size"], PARAMETERS["image_size"]))
        self.mask = Mask()
        self.mask.auto_gen_mask(self.original_img)
        
    
    def __call__(self, population: set):
        # try:
            result_img = StringArtDrawer(self.original_img)
            result_img.Decode(population)
            return self.__evaluate(result_img.draw_image)
        # except Exception as e:
        #     print(e)
        #     return -1


    def __evaluate(self, result_img: np.ndarray):
        
        if PARAMETERS["ev_mode"] == "DHash":
            return self.DHash(result_img)
        elif PARAMETERS["ev_mode"] == "one_pixel_diff":
            return self.one_pixel_diff(result_img)
        elif PARAMETERS["ev_mode"] == "mask_diff":
            return self.mask_diff(result_img)
        else:
            print("no match evaluate mode")

    def __dhash(self, img):
        # calculate the difference hash of the image
        img = cv2.resize(img, (PARAMETERS["Dhash_size"] + 1, PARAMETERS["Dhash_size"]))
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
    
    def one_pixel_diff(self, result_img):
        # calculate the difference between the original image and the result image
        diff = np.sum(np.abs(self.original_img - result_img))
        return diff
    


    def mask_diff(self, result_img):
        diff = (np.abs(self.original_img - result_img) ** 2) * self.mask.mask
        # print(diff)
        diff = np.sum(diff)
        return diff
    

class Mask:
    def __init__(self):
        self.mask = self.mask_bitmap = np.zeros((PARAMETERS["image_size"], PARAMETERS["image_size"]), dtype=np.uint8)
    def manual_mask(self):
        ### Mask ### 
        mask_img = cv2.imread("./test/mask.png")
        mask_img = cv2.resize(mask_img, (PARAMETERS["image_size"], PARAMETERS["image_size"]), interpolation=cv2.INTER_NEAREST)
        # Ensure the mask image is in grayscale
        mask_img_gray = cv2.cvtColor(mask_img, cv2.COLOR_BGR2GRAY)
        # Create an empty mask_bitmap with the same size as the image
        mask_bitmap = np.zeros_like(mask_img_gray, dtype=np.uint8)
        # Set pixels to 1 where the original mask is not white (255)
        mask_bitmap[mask_img_gray != 255] = 2
        self.mask = mask_bitmap

    def auto_gen_mask(self, ori_img):
        ret, binary_image = cv2.threshold(ori_img, 127, 255, cv2.THRESH_BINARY)
        mask_bitmap = np.zeros_like(binary_image, dtype=np.uint8)
        mask_bitmap[binary_image != 255] = 2

        self.mask = mask_bitmap * PARAMETERS["mask_coeff"]
        # 显示原始图像和二值化后的图像
        cv2.imshow('Image', binary_image)

        # 等待用户按键并关闭所有窗口
        cv2.waitKey(10)
        cv2.destroyAllWindows()