#!/usr/bin/env python
import cv2
import numpy as np

class ThreadTone():
    def __init__(self, imgPath, numPins, numLines, lineWidth):
        # Parameters
        imgRadius = 500         # Number of pixels that the image radius is resized to
        minLoop = 3             # Disallow loops of less than minLoop lines
        lineWeight = 15         # The weight a single thread has in terms of "darkness"
        initPin = 0             # Initial pin to start threading from

        self.numPins = numPins
        self.numLines = numLines
        self.lineWidth = lineWidth

        self.value = 0.0

        # Load image
        image = cv2.imread(imgPath)

        # Crop image
        height, width = image.shape[0:2]
        minEdge= min(height, width)
        topEdge = int((height - minEdge)/2)
        leftEdge = int((width - minEdge)/2)
        imgCropped = image[topEdge:topEdge+minEdge, leftEdge:leftEdge+minEdge]

        # Convert to grayscale
        imgGray = cv2.cvtColor(imgCropped, cv2.COLOR_BGR2GRAY)

        # Resize image
        imgSized = cv2.resize(imgGray, (2*imgRadius + 1, 2*imgRadius + 1)) 

        # Invert image
        imgInverted = self.invertImage(imgSized)

        # Mask image
        imgMasked = self.maskImage(imgInverted, imgRadius)

        # Define pin coordinates
        coords = self.pinCoords(imgRadius, numPins)
        height, width = imgMasked.shape[0:2]

        # Initialize variables
        i = 0
        lines = []
        previousPins = []
        oldPin = initPin
        lineMask = np.zeros((height, width))

        self.imgResult = 255 * np.ones((height, width))

        # Loop over lines until stopping criteria is reached
        for line in range(numLines):
            i += 1
            bestLine = 0
            oldCoord = coords[oldPin]

            # Loop over possible lines
            for index in range(1, numPins):
                pin = (oldPin + index) % numPins

                coord = coords[pin]

                xLine, yLine = self.linePixels(oldCoord, coord)

                # Fitness function
                lineSum = np.sum(imgMasked[yLine, xLine])

                if (lineSum > bestLine) and not(pin in previousPins):
                    bestLine = lineSum
                    bestPin = pin

            # Update previous pins
            if len(previousPins) >= minLoop:
                previousPins.pop(0)
            previousPins.append(bestPin)

            # Subtract new line from image
            lineMask = lineMask * 0
            cv2.line(lineMask, oldCoord, coords[bestPin], lineWeight, lineWidth)
            imgMasked = np.subtract(imgMasked, lineMask)

            # Save line to results
            lines.append((oldPin, bestPin))

            # plot results
            xLine, yLine = self.linePixels(coords[bestPin], coord)
            self.imgResult[yLine, xLine] = 0

            # Break if no lines possible
            if bestPin == oldPin:
                break

            # Prepare for next loop
            oldPin = bestPin

    # Invert grayscale image
    def invertImage(self, image):
        return (255-image)

    # Apply circular mask to image
    def maskImage(self, image, radius):
        y, x = np.ogrid[-radius:radius + 1, -radius:radius + 1]
        mask = x**2 + y**2 > radius**2
        image[mask] = 0

        return image

    # Compute coordinates of loom pins
    def pinCoords(self, radius, numPins=200, offset=0, x0=None, y0=None):
        alpha = np.linspace(0 + offset, 2*np.pi + offset, numPins + 1)

        if (x0 == None) or (y0 == None):
            x0 = radius + 1
            y0 = radius + 1

        coords = []
        for angle in alpha[0:-1]:
            x = int(x0 + radius*np.cos(angle))
            y = int(y0 + radius*np.sin(angle))

            coords.append((x, y))
        return coords

    # Compute a line mask
    def linePixels(self, pin0, pin1):
        length = int(np.hypot(pin1[0] - pin0[0], pin1[1] - pin0[1]))

        x = np.linspace(pin0[0], pin1[0], length)
        y = np.linspace(pin0[1], pin1[1], length)

        return (x.astype(int)-1, y.astype(int)-1)
