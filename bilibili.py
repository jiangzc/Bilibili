import requests
import json
import rsa
import base64
import random
import sys
import os
import time


PATH = os.path.abspath(os.path.dirname(sys.argv[0]))

def _rsa_encrypt(pubkey, hash, password):
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey)
    password = hash + password
    return base64.b64encode(rsa.encrypt(password.encode('utf-8'), pubkey))

def get_CN_time():
    return time.asctime(time.gmtime(time.time() + 8 * 60 * 60))

def log(string):
    with open(os.path.join(PATH, 'log.txt'), 'a') as f:
        f.write(string + '\r\n')


class Bilibili(object):

    def __init__(self):
        self.session = requests.session()
        self.session.get('https://account.bilibili.com/login')

    def _get_vcode(self):
         res = self.session.get('https://passport.bilibili.com/captcha')
         with open('vcode.png', 'wb') as f:
             f.write(res.content)

    def _get_key(self):
        res = self.session.get('https://passport.bilibili.com/login?act=getkey')
        obj = json.loads(res.text)
        self.key = obj['key']
        self.hash = obj['hash']

    def check_login(self, output=1):
        self.session.get('http://www.bilibili.com/')
        cookies = self.session.cookies.get_dict()
        if 'DedeUserID' in cookies.keys():
            if output:
                print('isLogin = True, ID=', cookies['DedeUserID'])
            return True
        else:
            if output:
                print('isLogin = False')
            return False

    def dumps(self, filename):
        print('dumping in file...')
        filename = os.path.join(PATH, filename)
        with open(filename, 'w') as f:
            cookie = self.session.cookies.get_dict()
            f.write(json.dumps(cookie))

    def loads(self, filename):
        print('loading from file...')
        filename = os.path.join(PATH, filename)
        try:
            with open(filename, 'r') as f:
                cookie = json.loads(f.read())
                self.session.cookies.update(cookie)
        finally:
            return self.check_login()

    def login(self, userid, password):
        self._get_vcode()
        self._get_key()
        vcode = input('input vcode:')
        self.session.post(url='https://passport.bilibili.com/login/dologin',
                          data={
                              'act': 'login',
                              'gourl': 'https://passport.bilibili.com/login/dologin',
                              'keeptime': '2592000',
                              'pwd': _rsa_encrypt(self.key, self.hash, password),
                              'userid': userid,
                              'vdcode': vcode
                          })
        return self.check_login()

    def give_coin(self, aid):
        self.session.headers.update({'Referer': 'http://www.bilibili.com/video/av' + str(aid)})
        res = self.session.post('http://www.bilibili.com/plus/comment.php',
                          data={
                              'aid': aid,
                              'multiply': 1,
                              'player': 1,
                              'rating': 100
                          })
        print('give 1 coin to aid:', aid, res.text)

    def get_video(self):
        res = self.session.get('http://api.bilibili.cn/recommend')
        obj = json.loads(res.text)
        L = [x['aid'] for x in obj['list']]
        return L

def main():
    user = Bilibili()
    #login
    if not user.loads('cookie.json'):
        user.login('末日V4', 'Q110110110')
        user.dumps('cookie.json')
    #give corn
    L = user.get_video()
    user.give_coin(L[random.randint(0, len(L))])
    ###
    log(get_CN_time() + ' started')

if __name__ == '__main__':
    main()
