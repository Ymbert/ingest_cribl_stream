import pycurl
import json
from io import BytesIO

headers = ['Accept: application/json']
buffer = BytesIO()

c = pycurl.Curl()
c.setopt(c.URL, 'https://www.covid19dataportal.org/api/backend/viral-sequences/sequences?page=1&size=15&format=JSON')
c.setopt(c.HTTPHEADER, headers)
c.setopt(c.WRITEDATA, buffer)

c.perform()

headers = ['Content-Type: application/json', 'Authorization: Splunk 79547730-3474-616e-3577-54316d66714b']
data = json.loads(buffer.getvalue().decode('utf-8'))["entries"]

c.setopt(c.URL, 'https://[ingress-address]:[port]/services/collector')
c.setopt(c.HTTPHEADER, headers)

for entry in data:

    data_post = json.dumps({"event": entry, "sourcetype": "api"})

    c.setopt(c.POSTFIELDS, data_post)
    c.setopt(c.WRITEDATA, buffer)

    c.perform()

c.close()

response = buffer.getvalue()

print(response.decode('utf-8'))