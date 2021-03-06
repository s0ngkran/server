
import requests
import urllib.parse
import sys
import os
import time
class Line():
    
    def __init__(self, filename, turnoff=False):
        
        self.url = 'https://notify-api.line.me/api/notify'
        self.token = 'kic5BCvffrnTLGoPHhiITqUYwp8DEQxZPN18ouRG6wU'
        self.headers = {"Authorization":"Bearer "+self.token}
        self.filename = filename
        self.turnoff = turnoff
        # self.send('starting... ')
    def post(self, data, headers='', files=''):
        if not self.turnoff:
            if headers=='': headers=self.headers
            success = False
            while not success:
                try:
                    r = requests.post(self.url, headers=headers, data=data, files=files)
                    success = True
                    return r
                except:
                    print('requests not success wait 10 sec')
                    time.sleep(10)

    def send(self, msg):
        if not self.turnoff:
            msg = str(self.filename + '\n>>>' + msg)
            self.post({'message':msg})
        
            # print( r.text)
    def send_group(self, msg):
        if not self.turnoff:
            group_token = '38yvBf3KyRqRrOGj312UhycDcNGTPjNCOlTm9R9xuyU'
            headers = {"Authorization":"Bearer " + group_token}
            self.post({'message':msg}, headers=headers)
            # print( r.text)
    def test_send_group(self):
        if not self.turnoff:
            self.send_group('im notify')
    def test_send(self):
        if not self.turnoff:
            self.send('this is a test msg.')
            print('sent.')

    def send_img(self, img, text='img from server'):
        if not self.turnoff:
            data = ({'message':text})
            f = {'imageFile':open(img,'rb')}
            self.post(data, files=f)
            # print(r.text)
    def send_torch(self, tensor):
        if not self.turnoff:
            import torch2img 
            torch2img.write(tensor)
            self.send_img('temp.jpg')
    def test_send_torch(self):
        if not self.turnoff:
            import torch
            t = torch.rand([100,100])
            self.send_torch(t)

if __name__ == '__main__':
    line = Line(os.path.basename(__file__))
    line.test_send_torch()
    