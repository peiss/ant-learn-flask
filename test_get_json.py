import requests

url = "http://127.0.0.1:5000/getjson"

r = requests.get(url)

print(r.status_code)
#print(r.text)

import json
#print(json.loads(r.text))
for row in json.loads(r.text):
    print(row)