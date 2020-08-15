
import requests
import urllib.parse
import sys
import os
class Line():
    def __init__(self, filename):

        self.url = 'https://notify-api.line.me/api/notify'
        self.token = 'kic5BCvffrnTLGoPHhiITqUYwp8DEQxZPN18ouRG6wU'
        self.headers = {"Authorization":"Bearer "+self.token}
        self.filename = filename

    def send(self, msg):
        msg = str(self.filename + '\n>' + msg)
        r = requests.post(self.url, headers=self.headers , data = {'message':msg})
        # print( r.text)
    def test_send(self):
        self.send('this is a test msg.')
        print('sent.')

    def send_img(self, img):
        data = ({'message':'Test Image'})
        f = {'imageFile':open(img,'rb')}
        r = requests.post(self.url, headers=self.headers, data=data, files=f)
        print(r.text)
    def send_torch(self, tensor):
        import torch2img 
        torch2img.write(tensor)
        self.send_img('temp.jpg')
    def test_send_torch(self):
        import torch
        t = torch.rand([100,100])
        self.send_torch(t)

if __name__ == '__main__':
    line = Line('test.py')
    line.test_send()
    