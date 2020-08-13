
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
def test():
    send('this is a test msg.')
    print('sent.')
def send_img(img):
    data = ({'message':'Test Image'})
    f = {'imageFile':open(img,'rb')}
    r = requests.post(url, headers=headers, data=data, files=f)
    print(r.text)


if __name__ == '__main__':
    test()