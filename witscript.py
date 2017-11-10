import requests
import json
# put your keys in the header
headers = {
    "app_id": "f9194057",
    "app_key": "200d4c4528b949a99f4dbe7f6154120b"
}


image_url = "https://scontent.xx.fbcdn.net/v/t34.0-12/23416125_1612002012156608_1751693873_n.png?_nc_ad=z-m&_nc_cid=0&oh=e09872c2fbbd17e1770840dcd6d03658&oe=5A068710"
payload = '{"image":"'+image_url+'"}'

url = "http://api.kairos.com/detect"

# make request
r = requests.post(url, data=payload, headers=headers)
val = json.loads(r.content)
print val['images'][0]['faces'][0]['attributes']['gender']['type']
print val['images'][0]['faces'][0]['attributes']['age']
