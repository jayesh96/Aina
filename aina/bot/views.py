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
from messenger_scripts import post_facebook_face_message,post_facebook_location_message

PAGE_ACCESS_TOKEN = "EAAaVROdQybwBAIpbQWgPTeZCJ2P0ZBvaimOcP6CGBBcHiQCLraRAp6cCSCoo5SgLZCdbeTq5ZBStZAas5mZCqxNEIGiBXwO11S2sAqfJpCUyWHYo1R2fVqDif2zxiMgpkR4N0tKxzIyyZBkGM7uNbQwTYJO4YZCQBVqgg0OzjunUhAZDZD"
VERIFY_TOKEN = "30071196"

from wit import Wit
access_token = 'DHOSKLQAXGNVVPCC3UGXAPZJRCPVTHAY'
client = Wit(access_token)


# Helper function


# Create your views here.
class AinaBotView(generic.View):
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
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    
                    if 'attachments' in message['message']:
                        str =  message['message']['attachments']
                        for json_i in str:
                            
                            content_type = json_i['type']
                            if content_type == 'location':
                                message_coordinates = json_i['payload']['coordinates']
                                latitude = message_coordinates['lat']
                                longitude = message_coordinates['long']
                                print (latitude, longitude)
                                post_facebook_location_message(message['sender']['id'], latitude, longitude)
                            if content_type == 'image':
                                image_url = json_i['payload']['url']
                                val = face_detection(image_url)
                                if val[0] == "M":
                                    post_facebook_face_message(message['sender']['id'], "Hey You are a boy",val[1])
                                else:
                                    post_facebook_face_message(message['sender']['id'], "Hey You are a girl",val[1])
                                    
                                # post_facebook_message_image(message['sender']['id'], image_url)
                    # post_facebook_message(message['sender']['id'], message['message']['text'])   

        return HttpResponse()    










































def messagereturn(request,string):
    resp = None
    # resp = client.message('what is the weather in London?')
    return JsonResponse({'foo':'bar'})


def getvoiceresponse(request):
    if request.method=="POST":
        
        resp = index()
        return render(request, 'index.html', {"resp":resp})
    return render(request, 'index.html', {})
