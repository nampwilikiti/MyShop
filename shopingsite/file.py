import os
import requests

ip = requests.get('https://ipinfo.io/')
data = ip.json()
location =data['loc'],split(',')
lat =float(location[1])
log =float(location[0])