import cv2
import json
import os

def browseImages(images, basePath, user_id):
    i = 0
    while (i >= 0 and i < len(images)):
        image = images[i]
        print 'Photo ' + str(i + 1) + ' of ' + str(len(images))
        image['img'] = cv2.imread(image['path'] + '/' + image['filename'])
        key = getKeypressResultFromImage(image['filename'], image['img'])

        if key == 121:
            print 'Like saved to: ' + basePath + '/yes/'
            writeYesOrNoForImages(True, basePath, user_id, images)
            return True

        elif key == 110:
            print 'Pass saved to: ' + basePath + '/no/'
            writeYesOrNoForImages(False, basePath, user_id, images)
            return False

        elif key == 2555904:
            if not i == len(images) - 1:
                i += 1

        elif key == 2424832:
            if not i == 0:
                i -= 1
        else:
            print 'Invalid key (use left/right to navigate, y/n to like/pass)'

def writeYesOrNoForImages(yes, path, user_id, images):
    for index, image in enumerate(images):
        if not 'img' in image:
            image['img'] = cv2.imread(image['path'] + '/' + image['filename'])
        if (yes and 'img' in image):
            cv2.imwrite(path + '/yes/' + str(user_id) + '_' + str(index) + '.png', image['img'])
        else:
            cv2.imwrite(path + '/no/' + str(user_id) + '_' + str(index) + '.png', image['img'])
        os.remove(path + '/' + str(user_id) + '/' + image['filename'])
    os.rmdir(path + '/' + str(user_id) + '/')

def getKeypressResultFromImage(filename, img):
    cv2.namedWindow(filename)
    print filename, img
    cv2.imshow(filename, img)
    k = cv2.waitKey()
    cv2.destroyWindow(filename)
    return k


if __name__ == '__main__':
    with open('config.json') as cfg:
        config = json.load(cfg)

    path = config['image_folder_path'] + '/detected'

    images = []
    for filename in os.listdir(path):
        data = {
            'filename': filename,
            'path': path,
        }
        images.append(data)

        #os.remove(path + '/' + filename)
    browseImages(images)
