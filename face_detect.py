import cv2
import sys
import os
import numpy

def readImageAndDetectFaces(imageBuf, basePath, filename, cascPath):
    faces = []

    # Read the image
    image = cv2.imdecode(imageBuf, -1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x = 0.75
    scale = 2 ** x
    # Detect faces in the image
    faces = detectFaces(gray, scale, cascPath)
    count = 0

    while (len(faces) != 1 and count < 29):
        x -= 0.025
        scale = 2 ** x
        count += 1
        faces = detectFaces(gray, scale, cascPath)

    if (len(faces) == 1):
        for (x, y, w, h) in faces:
            cropped = image[y:y+h, x:x+w]
        resized = cv2.resize(cropped, (120, 120), interpolation = cv2.INTER_AREA)
        cv2.imwrite(basePath + '/detected/' + filename, resized)
        if (isAttractive(cropped)):
            print 'she cute'

    return len(faces)


    # Don't do anything else yet
    # maybe when we have an isAttractive function
    # else:



def detectFaces(gray, scale, cascPath):
    faceCascade = cv2.CascadeClassifier(cascPath)
    return faceCascade.detectMultiScale(
        gray,
        scaleFactor=scale,
        minNeighbors=5,
        minSize=(120, 120),
        maxSize=(600, 600),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

def isAttractive(face):
    return False

if __name__ == '__main__':

    # Get user supplied values
    imagePath = sys.argv[1]
    cascPath = sys.argv[2]

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    print "Found {0} faces!".format(len(faces))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Faces found", image)
    cv2.waitKey(0)
