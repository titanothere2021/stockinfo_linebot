# -- coding: utf-8 --
import requests
import json
from datetime import datetime
import time

def lineNotifyMessage(msg):
    token = 'tUTkhYP3qvhNH8WBatXSLaUuXeUTD3abAhuZjo1j0rg'
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code
