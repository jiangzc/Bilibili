#Login Bilibili

##Requirment
-python3

-requests Lib

##Initialize
```python
user = Bilibili()
```

##Login
```python
user.login('userid', 'password')
```
The Verification Code will be saved in .\vcode.png

Open the file and enter the vcode
```
vcode:*****
```
If you succeed in login, it will output "isLogin = True, ID=******" after a few seconds

Else output "isLogin = False"

##Dumps
Save cookies
```python
user.dumps('cookie.json')
```
##Loads
Load cookies
```python
user.loads('cookie.json')
```
##Check Login
```python
user.check_login()
```