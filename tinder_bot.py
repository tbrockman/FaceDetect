# encoding: utf8                                                                                                                                           1,1           Top# encoding: utf8
import argparse
from datetime import datetime
import json
from random import randint
from random import choice
import requests
import sys
from time import sleep
import shutil
import os
import urllib
import face_detect
import numpy

with open('secret.json') as sec:
    secret = json.load(sec)

with open('config.json') as cfg:
    config = json.load(cfg)

headers = {
    'app_version': '3',
    'platform': 'ios'
}

fb_id = secret['fb_id']
fb_auth_token = secret['fb_auth_token']
path = config['image_folder_path']
casc_path = config['cascade_path']
locations = config['locations']
faces = {
    'one_face_only': 0,
    'no_faces': 0,
    'more_than_one': 0
}

class User(object):
    def __init__(self, data_dict):
        self.d = data_dict

    @property
    def user_id(self):
        return self.d['_id']

    @property
    def photos(self):
        return self.d['photos']

    @property
    def bio(self):
        try:
            x = self.d['bio'].encode('ascii', 'ignore').replace('\n', '')[:50].strip()
        except (UnicodeError, UnicodeEncodeError, UnicodeDecodeError):
            return '[garbled]'
        else:
            return x


    @property
    def age(self):
        raw = self.d.get('birth_date')
        if raw:
            d = datetime.strptime(raw, '%Y-%m-%dT%H:%M:%S.%fZ')
            return datetime.now().year - int(d.strftime('%Y'))

        return 0

    def __unicode__(self):
        return u'{name} ({age}), {distance}km, {photos}'.format(
            name=self.d['name'],
            age=self.age,
            distance=self.d['distance_mi'],
            photos=self.photos
        )

def facebookLogin():
    newHeaders = {
        'User-Agent' : 'Mozilla/5.0'
    }
    req = requests.get(
    'https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token',
    headers=newHeaders
    )
    print(json.dumps(req.json()))



def auth_token(fb_auth_token, fb_user_id):
    h = headers
    h.update({'content-type': 'application/json'})
    req = requests.post(
        'https://api.gotinder.com/auth',
        headers=h,
        data=json.dumps({'facebook_token': fb_auth_token, 'facebook_id': fb_user_id})
    )
    try:
        return req.json()['token']
    except:
        return None

def getUserPhotos(user, auth_token):
    h = headers
    h.update({'X-Auth-Token': auth_token})
    for index, photo in enumerate(user.photos):
        imageUrl = photo['url']

        req = urllib.urlopen(imageUrl)
        arr = numpy.asarray(bytearray(req.read()), dtype=numpy.uint8)

        filename = str(user.user_id) + '_' + str(index) + '.png'
        faceCount = face_detect.readImageAndDetectFaces(arr, path, filename, casc_path)
        if (faceCount > 1):
            faces['more_than_one'] += 1
        elif (faceCount == 1):
            faces['one_face_only'] += 1
        else:
            faces['no_faces'] += 1

        print(faces)

def changeLocation(lat, long, auth_token):
    h = headers
    h.update({'X-Auth-Token': auth_token})
    h.update({'content-type': 'application/json'})
    req = requests.post(
    'https://api.gotinder.com/user/ping',
    headers=h,
    data=json.dumps({"lat": lat, "lon": long})
    )

    try:
        return
    except:
        return None

def getProfile(auth_token):
    h = headers
    h.update({'X-Auth-Token': auth_token})
    h.update({'content-type': 'application/json'})
    req = requests.get(
    'https://api.gotinder.com/profile',
    headers=h
    )
    try:
        return req.json()
    except:
        return None

def recommendations(auth_token):
    h = headers
    h.update({'X-Auth-Token': auth_token})
    r = requests.get('https://api.gotinder.com/user/recs', headers=h)
    if r.status_code == 401 or r.status_code == 504:
        raise Exception('Invalid code')
        print r.content

    if not 'results' in r.json():
        print r.json()
        sleep(1800)
        return

    for result in r.json()['results']:
        yield User(result)


def like(user_id):
    try:
        u = 'https://api.gotinder.com/like/%s' % user_id
        d = requests.get(u, headers=headers, timeout=0.7).json()
    except KeyError:
        raise
    else:
        return d['match']


def nope(user_id):
    try:
        u = 'https://api.gotinder.com/pass/%s' % user_id
        requests.get(u, headers=headers, timeout=0.7).json()
    except KeyError:
        raise


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Tinder automated bot')
    parser.add_argument('-l', '--log', type=str, default='activity.log', help='Log file destination')

    args = parser.parse_args()

    print 'Tinder bot'
    print '----------'
    matches = 0
    liked = 0
    nopes = 0
    locationCounter = 1

    while True:
        token = auth_token(fb_auth_token, fb_id)
        locationCounter -= 1
        if (locationCounter == 0):
            newCity = choice(locations.keys())
            locationCounter = randint(1000, 2000)
            print 'changing location to: ' + newCity
            changeLocation(locations[newCity]['lat'], locations[newCity]['lon'], token)
            sleep(5)

        if not token:
            print 'could not get token'
            sys.exit(0)

        for user in recommendations(token):
            if not user:
                break

            getUserPhotos(user, token)

            try:

                break
                # action = like_or_nope()
                # if action == 'like':
                #     print ' -> Like'
                #     match = like(user.user_id)
                #     if match:
                #         print ' -> Match!'
                #
                #     with open('./liked.txt', 'a') as f:
                #         f.write(user.user_id + u'\n')
                #
                # else:
                #     print ' -> random nope :('
                #     nope(user.user_id)

            except:
                print 'networking error %s' % user.user_id

        s = float(randint(1000, 3000) / 1000)
        sleep(s)
