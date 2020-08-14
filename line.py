
import requests
import urllib.parse
import sys
url = 'https://notify-api.line.me/api/notify'
token = 'kic5BCvffrnTLGoPHhiITqUYwp8DEQxZPN18ouRG6wU'
headers = {"Authorization":"Bearer "+token}
def send(msg):
    msg = str(msg)
    r = requests.post(url, headers=headers , data = {'message':msg})
    # print( r.text)
def test_send():
    send('this is a test msg.')
    print('sent.')

def send_img(img):
    data = ({'message':'Test Image'})
    f = {'imageFile':open(img,'rb')}
    r = requests.post(url, headers=headers, data=data, files=f)
    print(r.text)
def send_torch(tensor):
    import torch2img 
    torch2img.write(tensor)
    send_img('temp.jpg')
def test_send_torch():
    import torch
    t = torch.rand([100,100])
    send_torch(t)

if __name__ == '__main__':
    test_send()
    