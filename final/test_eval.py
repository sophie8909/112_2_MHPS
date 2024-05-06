import cv2
from Evaluate import Evaluate
# Testing
# Evaluate the result
photo = cv2.imread("./test/photo.png")
result = cv2.imread("./test/144_4000.png")
print("img shape", result.shape)
ev = Evaluate(photo)
ev(result)