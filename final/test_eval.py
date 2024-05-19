import cv2
from Evaluate import Evaluate
import os

# Load the original image
photo = cv2.imread("./test/photo.png")
# read all images in the test folder
test_img = os.listdir("./test")
print(test_img)
for img in test_img:
    print(img)
    result = cv2.imread("./test/" + img)
    # initialize the Evaluate class with the original image
    ev = Evaluate(photo)
    # evaluate the result image using DHash
    value = ev.evaluate(result)
    print(value)
    