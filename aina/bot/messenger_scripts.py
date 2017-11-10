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

from other_scripts import restaurant_recommendor_engine,face_detection


PAGE_ACCESS_TOKEN = "EAAaVROdQybwBAIpbQWgPTeZCJ2P0ZBvaimOcP6CGBBcHiQCLraRAp6cCSCoo5SgLZCdbeTq5ZBStZAas5mZCqxNEIGiBXwO11S2sAqfJpCUyWHYo1R2fVqDif2zxiMgpkR4N0tKxzIyyZBkGM7uNbQwTYJO4YZCQBVqgg0OzjunUhAZDZD"
VERIFY_TOKEN = "30071196"

from wit import Wit
access_token = 'DHOSKLQAXGNVVPCC3UGXAPZJRCPVTHAY'
client = Wit(access_token)


def post_facebook_face_message(fbid, recevied_message,age):
    # Remove all punctuations, lower case the text and split it based on space
     
    print(age)
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json() 
    text = 'Yo '+user_details['first_name']+'..! ' + str(recevied_message)
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    response_msg = json.dumps(
                    {
                        "recipient":
                            {
                                "id":fbid
                            }, 
                        "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text":"Want To Know more about Your Face?",
        "buttons":[
          {
            "type":"web_url",
            "url":"http://mashglobal.org/",
            "title":"Show Website"
          },
          {
            "type":"web_url",
            "url":"http://mashglobal.org/",
            "title":"Age Around "+str(age)+" years"
            
          }
        ]
      }
    }
  }
                            })

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

    pprint(status.json())


############################################## LOCATION BASED RECOMMENDATIONS ############################################################


def post_facebook_location_message(fbid, latitude, longitude):
    # Remove all punctuations, lower case the text and split it based on space
    string = str(latitude) + " , " + str(longitude)
    print (string)

    data = restaurant_recommendor_engine(latitude,longitude)
    print data

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json() 
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN

    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":"Some Restaurants Recommendation Based On your Age and Location"}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    elements = []

    for i in range(4):
        restaurant_name = data["nearby_restaurants"][i]['restaurant']['name']
        rating = data["nearby_restaurants"][i]['restaurant']['user_rating']["aggregate_rating"]
        address = data["nearby_restaurants"][i]['restaurant']["location"]["locality_verbose"]
        url = data["nearby_restaurants"][i]['restaurant']["url"]
        elments_list = {
                "title": restaurant_name,
                "subtitle": address,
                "image_url": "",          
                "buttons": [
                  {
                    "title": "Rating:"+rating,
                    "type": "web_url",
                    "url": url,
                    "messenger_extensions": True,
                    "webview_height_ratio": "tall",
                    "fallback_url": "https://www.google.co.in/?gfe_rd=cr&dcr=0&ei=87oEWpCeJNCL8QfG4Y7oDw"            
                  },

                ]
              }
        elements.append(elments_list)


    response_msg = json.dumps({
  "recipient":{
    "id":fbid
  }, 
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "list",
        "top_element_style": "compact",

        "elements": elements,
         "buttons": [
          {
            "title": "RESTAURANTS",
            "type": "postback",
            "payload": "payload"            
          }
        ]  
      }
    }
  }
})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())



############################################## LOCATION BASED RECOMMENDATIONS ############################################################
