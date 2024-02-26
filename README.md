# door_dash_bot

```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/Users/ekim/Library/Application Support/Google/Chrome/Profile 2"
```

```
conda activate bots
python -m src.app.test
```
```
ps aux | grep chrome\n


lsof -i -P -n | grep <PID>

```


```


[//]: # (export DD_MERCHANT_LOGIN_URL='https://www.doordash.com/merchant/orders?business_id=12345678')
[//]: # (export DEV_LOGIN_EMAIL='ekim@domain.com')
[//]: # (export DEV_LOGIN_PASSWORD='someDevPassword')
```

Via terminal

 (linux/unix)
```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/Users/ekim/Library/Application Support/Google/Chrome/Profile 2" https://www.doordash.com/merchant/orders?business_id=12345678
```

Windows
```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\ekim\AppData\Local\Google\Chrome\User Data" https://www.doordash.com/merchant/orders?business_id=12345678
```

For better UX, will need to have the desktop browser shortcut (w/ chrome browser icon and perhaps even a overlayed text to indicate its specified use case for this bot) pre-configured via properties/settings of said shortcut


- Shortcut should be configured to access `https://www.doordash.com/merchant/orders?business_id=12345678` as script picks up from browser on Orders page

file dump path
```
G:\Imports\IR\Door Dash\DD Daily Order Details
```

NOTE: Chromedriver executable paths may vary. Confirm it is configured correctly according to your machine.
###  src.app.drivers
```
_get_chromedriver_executable_path()
        
BOTS VM : 'C:\\chromedriver-win64\\chromedriver.exe'
HOST Windows: 'C:\\Users\\ekima\\AppData\\Local\\anaconda3\\envs\\bots\\Lib\\site-packages\\seleniumbase\\drivers\\chromedriver.exe' ?
Mac i9: /usr/local/bin/chromedriver
Mac M1: /opt/homebrew/bin/chromedriver

```



