# yomamabot/fb_yomamabot/views.py
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from clarifai.rest import ClarifaiApp

#  ------------------------ Fill this with your page access token! -------------------------------
PAGE_ACCESS_TOKEN = "EAADKGhPh2u0BACAJ6hCHArGbnukjVNQdZAVOmZC1aNuxCtqzuFlM1Shzjn95VdvEkIHvEwaY1OcipuOxKbDRxZBgfczBH7pDVgLy6vFcJGr5322M4dMGrHoVP0PgWGBSfLVcIkZCk8XigZBt2ZAUvBl69ZAtTBfl0q5D1QPoNlbRgZDZD"
VERIFY_TOKEN = "2318934571"


flowers = ['rose', 'sunflower', 'cauliflower', 'lotus']
# Helper function

def post_facebook_message_continue_chatting(fbid):
    # Remove all punctuations, lower case the text and split it based on space
    

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json() 
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
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
        "text":"What do you want to do next?",
        "buttons":[
          {
            "type":"web_url",
            "url":"http://mashglobal.org/",
            "title":"Show Website"
          },
          {
            "type":"postback",
            "title":"Post a Picture",
            "payload":"USER_DEFINED_PAYLOAD"
          }
        ]
      }
    }
  }
                            })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


def post_facebook_message(fbid, latitude, longitude):
    # Remove all punctuations, lower case the text and split it based on space
    string = str(latitude) + " , " + str(longitude)
    print (string)

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json() 
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps(
                    {
                        "recipient":
                            {
                                "id":fbid
                            }, 
                        "message":
                            {
                                "text":string
                            }
                            })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


def post_facebook_message_text(fbid, text):
    # Remove all punctuations, lower case the text and split it based on space
    string = "Click Here On any Option"
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json() 
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps(
                    {
                        "recipient":
                            {
                                "id":fbid
                            }, 
                        "message":
                            {
                                "text":string,
                                "quick_replies":[
                                 {
                                "content_type":"text",
                                  "title":"About",
                               "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                                },
                            {
                                  "content_type":"text",
                                      "title":"Help",
                                  "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"
                                     },
                                {

                                  "content_type":"text",
                                      "title":"Continue Chatting",
                                  "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"
                                     }

                         ]
                            }
                            })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())    

def post_facebook_message_text_about(fbid, about_command):
    # Remove all punctuations, lower case the text and split it based on space
    string = "This Bot is used to get images from the user and then used to analyze and study about the flower and plants.This is a great tool for students to learn and for kids to explore new flowers and plants"

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json() 
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps(
                    {
                        "recipient":
                            {
                                "id":fbid
                            }, 
                        "message":
                            {
                                "text":string
                            }
                            })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


######################  HANDLING IMAGES ###############################
def post_facebook_message_image(fbid, image_url):
    # Remove all punctuations, lower case the text and split it based on space
    a = []

    app = ClarifaiApp("7IytkvcgtC3tBdxY2cjR-jF9kJD1rDlZYh5o5tcq", "xMlF4W-tepNUh4jHf7oouTSgqCvsphugB3iveNRG")
    model = app.models.get("general-v1.3")
    str = model.predict_by_url(url=image_url)
    print("$$$$$$$$$$$$$$$")
    str = str['outputs']
    for i in str:
        outputs = i['data']['concepts']

    for output in outputs:
        val = output['name']
        a.append(val)

    print(a)
    print("$$$$$$$$$$$$$")


    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json() 
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps(
                    {
                        "recipient":
                            {
                                "id":fbid
                            }, 
                        "message":
                            {
                                "text":image_url
                            }
                            })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

######################  HANDLING IMAGES ###############################



# Create your views here.
class YoMamaBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)   
                    # post_facebook_message(message['sender']['id'], message['message']['text'])      
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    if 'attachments' in message['message']:
                        str =  message['message']['attachments']
                        for json_i in str:
                            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                            print(json_i)
                            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                            
                            content_type = json_i['type']
                            if content_type == 'location':
                                message_coordinates = json_i['payload']['coordinates']
                                latitude = message_coordinates['lat']
                                longitude = message_coordinates['long']
                                print (latitude, longitude)
                                post_facebook_message(message['sender']['id'], latitude, longitude)
                            if content_type == 'image':
                                image_url = json_i['payload']['url']
                                post_facebook_message_image(message['sender']['id'], image_url)

                    else:
                        help_command = (message['message']['text'])
                        if help_command == "Get Started":
                            post_facebook_message_text(message['sender']['id'], help_command)
                        elif help_command == "About":
                            post_facebook_message_text_about(message['sender']['id'], help_command)
                        elif(help_command == "Continue Chatting"):
                            post_facebook_message_continue_chatting(message['sender']['id'])
                        else:
                            pass


        return HttpResponse()    






# {u'message':
#    {u'attachments':
#        [{u'payload': 
#           {u'coordinates': 
#               {u'lat': 28.69694,
#                 u'long': 77.189583
#                 }
#             },
#        u'title': u"Jayesh's Location",
#        u'type': u'location',
#        u'url': u'https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.bing.com%2Fmaps%2Fdefault.aspx%3Fv%3D2%26pc%3DFACEBK%26mid%3D8100%26where1%3D28.69694%252C%2B77.189583%26FORM%3DFBKPL1%26mkt%3Den-US&h=ATPHC_07DXGXz94-MYaLuhRp9Trn6deVvusyzzoZU91wB7umR5JduyV9vgysBQJ3PJPWx26wsWni0X3f1cUUwjhMWKrhhynzlxyT_RRGCJaeQLrQglbphkbOGMUFxGKAsHDN_mk&s=1&enc=AZPWTgyIBzM-cMgUjjhDVfd4kHOHoUPjHYPqiAfmT9tkNx5j-Ig4MQR6U4RdsVyIoJKKsGqu0IzdtQD6l14mSEQc'
#       }],
#   u'mid': u'mid.1485969512107:43be98ba56',
#   u'seq': 99601},
#  u'recipient': {u'id': u'1664819267163136'},
#  u'sender': {u'id': u'1290682247622958'},
#  u'timestamp': 1485969512107}


# {
#   u'message': 
#       {
#       u'mid': u'mid.1485970133711:f51478c063',
#         u'seq': 99613,
#         u'text': u'G'
#         },
#   u'recipient': {
#           u'id': u'1664819267163136'
#           },
#   u'sender': {
#       u'id': u'1290682247622958'
#       },
#   u'timestamp': 1485970133711
#  }


# {
#   "sender":{
#     "id":"USER_ID"
#   },
#   "recipient":{
#     "id":"PAGE_ID"
#   },
#   "timestamp":1458692752478,
#   "message":{
#     "mid":"mid.1458696618141:b4ef9d19ec21086067",
#     "seq":51,
#     "attachments":[
#       {
#         "type":"image",
#         "payload":{
#           "url":"IMAGE_URL"
#         }
#       }
#     ]
#   }
# }    