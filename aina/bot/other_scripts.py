from django.shortcuts import render

# Create your views here.
import json, requests, random, re
from pprint import pprint

from django.views import generic
import requests

from django.http.response import HttpResponse
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

import requests
from pprint import pprint



PAGE_ACCESS_TOKEN = "EAAaVROdQybwBAIpbQWgPTeZCJ2P0ZBvaimOcP6CGBBcHiQCLraRAp6cCSCoo5SgLZCdbeTq5ZBStZAas5mZCqxNEIGiBXwO11S2sAqfJpCUyWHYo1R2fVqDif2zxiMgpkR4N0tKxzIyyZBkGM7uNbQwTYJO4YZCQBVqgg0OzjunUhAZDZD"
VERIFY_TOKEN = "30071196"

from wit import Wit
access_token = 'DHOSKLQAXGNVVPCC3UGXAPZJRCPVTHAY'
client = Wit(access_token)


def restaurant_recommendor_engine(lat,long):
    locationUrlFromLatLong = "https://developers.zomato.com/api/v2.1/geocode?lat="+str(lat)+"&lon="+str(long)
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "0013ed53c26c663763e4711898a20c18"}
    response = requests.get(locationUrlFromLatLong, headers=header)
    data = response.json()
    return data


def face_detection(image_url):
    headers = {
        "app_id": "f9194057",
        "app_key": "200d4c4528b949a99f4dbe7f6154120b"
    }

    payload = '{"image":"'+image_url+'"}'

    url = "http://api.kairos.com/detect"
    r = requests.post(url, data=payload, headers=headers)
    val = json.loads(r.content)
    return val['images'][0]['faces'][0]['attributes']['gender']['type'],val['images'][0]['faces'][0]['attributes']['age']
