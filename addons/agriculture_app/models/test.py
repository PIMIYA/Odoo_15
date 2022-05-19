import requests


url = "http://ec2-34-215-20-244.us-west-2.compute.amazonaws.com:58809/api/Record"
data = {"CropStatus": ""}
response = requests.post(url, json=data)
# _logger.info(response.json().get('SeqNumber'))
seq = response.json().get('SeqNumber')

print(seq)
