#Login Bilibili

##Requirment
-python3

-requests Lib

##Initialize 初始化
```python
user = Bilibili()
```

##Login 登陆
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

##Dumps 保存
Save cookies
```python
user.dumps('cookie.json')
```
##Loads 加载
Load cookies
```python
user.loads('cookie.json')
```
##Check Login 检查是否登陆
```python
user.check_login() # Output "isLogin=....." and Return Booleans
user.check_login(None) # No output and Return Booleans
user.check_login(None) # No output and Return Booleans
```
##Give Coin 投币
```python
user.give_coin('7319078') # Require the aid of video
```
