import requests


class APISender:

    def __init__(self, url="http://127.0.0.1:8000/api/sensors/"):
        self.url = url

    def send(self, data):
        try:
            requests.post(self.url, json=data, timeout=2)
        except Exception as e:
            print("API ERROR:", e)