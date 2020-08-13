
import requests
url = 'https://notify-api.line.me/api/notify'
token = 'kic5BCvffrnTLGoPHhiITqUYwp8DEQxZPN18ouRG6wU'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
def send(msg):
    msg = str(msg)
    r = requests.post(url, headers=headers , data = {'message':msg})
    # print( r.text)
def test():
    send('this is a test msg.')
    print('sent.')

if __name__ == '__main__':
    test()