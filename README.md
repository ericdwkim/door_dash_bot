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


[//]: # (export DD_MERCHANT_LOGIN_URL='https://www.doordash.com/merchant/orders?business_id=11495418')
[//]: # (export DEV_LOGIN_EMAIL='ekim@txbstores.com')
[//]: # (export DEV_LOGIN_PASSWORD='3%rV@c7ixWgYVn')
```

Via terminal

 (linux/unix)
```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/Users/ekim/Library/Application Support/Google/Chrome/Profile 2" https://www.doordash.com/merchant/orders?business_id=11495418
```

Windows
```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\ekim\AppData\Local\Google\Chrome\User Data" https://www.doordash.com/merchant/orders?business_id=11495418
```

For better UX, will need to have the desktop browser shortcut (w/ chrome browser icon and perhaps even a overlayed text to indicate its specified use case for this bot) pre-configured via properties/settings of said shortcut


- Shortcut should be configured to access `https://www.doordash.com/merchant/orders?business_id=11495418` as script picks up from browser on Orders page