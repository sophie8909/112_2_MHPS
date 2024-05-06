import cv2
from Evaluate import Evaluate
import os
# Testing
# Evaluate the result
photo = cv2.imread("./test/photo.png")
# read all images in the test folder
test_img = os.listdir("./test")
print(test_img)
for img in test_img:
    print(img)
    result = cv2.imread("./test/" + img)
    ev = Evaluate(photo)
    ev(result)