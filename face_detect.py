import cv2
import sys
import os
import numpy
import json

def readImageAndDetectFaces(imageBuf, basePath, filename, cascPath):
    faces = []

    # Read the image
    image = cv2.imdecode(imageBuf, -1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x = 0.75
    scale = 2 ** x
    # Detect faces in the image
    faces = detectCascade(gray, scale, (120, 120), (600, 600), cascPath)
    count = 0

    while (len(faces) != 1 and count < 29):
        x -= 0.025
        scale = 2 ** x
        count += 1
        faces = detectCascade(gray, scale, (120, 120), (600, 600), cascPath)

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

def readLocalImagesAndDetect(path, config):
    for filename in os.listdir(path):
        readImageAndDetectFeatures(path, filename, config)


def readImageAndDetectFeatures(path, filename, config):
    image = cv2.imread(path + '/' + filename, -1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detectFeatures(image, gray, 1.1, config)

def detectFeatures(regular, gray, scale, config):
    eyes = detectCascade(gray, scale, (5,5), (35, 35), config['eye_cascade'])
    for (ex,ey,ew,eh) in eyes:
        print 'drawing rect in eyes'
        cv2.rectangle(regular,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    nose = detectCascade(gray, scale, (5,5), (35, 35), config['nose_cascade'])
    for (ex,ey,ew,eh) in nose:
        print 'drawing rect in nose'
        cv2.rectangle(regular,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)
    mouth = detectCascade(gray, scale, (5,5), (45, 45), config['mouth_cascade'])
    for (ex,ey,ew,eh) in mouth:
        print 'drawing rect in mouth'
        cv2.rectangle(regular,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)
    smile = detectCascade(gray, scale, (5,5), (40, 40), config['smile_cascade'])
    for (ex,ey,ew,eh) in smile:
        print 'drawing rect in smile'
        cv2.rectangle(regular,(ex,ey),(ex+ew,ey+eh),(133,133,133),2)
    cv2.imshow('img',regular)
    cv2.waitKey(0)

def detectCascade(gray, scale, minSize, maxSize, cascPath):
    cascade = cv2.CascadeClassifier(cascPath)
    return cascade.detectMultiScale(
        gray,
        scaleFactor=scale,
        minNeighbors=5,
        minSize=minSize,
        maxSize=maxSize,
        flags = cv2.CASCADE_SCALE_IMAGE
    )

def isAttractive(face):
    return False

if __name__ == '__main__':

    with open('config.json') as cfg:
        config = json.load(cfg)

    readLocalImagesAndDetect('F:\Workspace\FaceDetect\images\detected', config)
