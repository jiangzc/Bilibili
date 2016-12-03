import requests
import json
import rsa
import base64


def _rsa_encrypt(pubkey, hash, password):
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey)
    password = hash + password
    return base64.b64encode(rsa.encrypt(password.encode('utf-8'), pubkey))

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
        with open(filename, 'w') as f:
            cookie = self.session.cookies.get_dict()
            f.write(json.dumps(cookie))

    def loads(self, filename):
        print('loading from file...')
        with open(filename, 'r') as f:
            cookie = json.loads(f.read())
            self.session.cookies.update(cookie)
        self.check_login()


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

def main():
    user = Bilibili()
    user.loads('cookie.json')
    user.give_coin('7319078')


if __name__ == '__main__':
    main()
