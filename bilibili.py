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

    def check_login(self):
        cookies = self.session.cookies.get_dict()
        if 'DedeUserID' in cookies.keys():
            print('isLogin = True, ID=', cookies['DedeUserID'])
            return True
        else:
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


def main():
    user = Bilibili()
    user.loads('cookie.json')

if __name__ == '__main__':
    main()
