# Exploit payload & client browser fingerprint server

```
usage: server.py [-h] [-p PORT] [-s] [-n HOST [HOST ...]]

Serves all files in './payloads' direcotry with optional self-signed cert, as well as a fingerprint server that mimics the apache 'It
works!' page, but actually fingerprints a browser.

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT
  -s, --ssl             Run server over SSL?
  -n HOST [HOST ...], --host HOST [HOST ...]
                        Hostname[s] (or IP[s]) for generated links
```

# Example run:
```
root@kali:/payload_server# ./server.py
[+] Fingerprint link(s): (really, anything except a file that exists)
http://172.17.0.2:8000/
http://172.17.0.2:8000/TwYCEvgMHs
http://kali.local:8000/
http://kali.local:8000/TwYCEvgMHs

[+] Available payloads:
http://172.17.0.2:8000/lin_x64_https.bin
http://172.17.0.2:8000/lin_x86_https.bin
http://172.17.0.2:8000/win_x64_https.dll
http://172.17.0.2:8000/win_x64_https.exe
http://172.17.0.2:8000/win_x64_https.ps1
http://172.17.0.2:8000/win_x64_tcp.exe
http://172.17.0.2:8000/win_x86_https.dll
http://172.17.0.2:8000/win_x86_https.exe
http://172.17.0.2:8000/win_x86_https.ps1
http://kali.local:8000/lin_x64_https.bin
http://kali.local:8000/lin_x86_https.bin
http://kali.local:8000/win_x64_https.dll
http://kali.local:8000/win_x64_https.exe
http://kali.local:8000/win_x64_https.ps1
http://kali.local:8000/win_x64_tcp.exe
http://kali.local:8000/win_x86_https.dll
http://kali.local:8000/win_x86_https.exe
http://kali.local:8000/win_x86_https.ps1

[+] Now all files in the 'payloads' directory and fingerprint server on port 8000
```

# Fingerprinting
Uses [JS Fingerprint 2](https://github.com/Valve/fingerprintjs2) and stores output in `logs/<client IP>.txt`

```
127.0.0.1 - - [29/Apr/2020 09:37:07] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [29/Apr/2020 09:37:07] "GET /app.js HTTP/1.1" 200 -
127.0.0.1 - - [29/Apr/2020 09:37:09] "GET /favicon.ico HTTP/1.1" 200 -
127.0.0.1 - - [29/Apr/2020 09:37:09] "POST / HTTP/1.1" 200 -
```

The last `POST` request is the client sending it's fingerprint data:
```
userAgent = Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101
Firefox/68.0
webdriver = false
language = en-US
colorDepth = 24
deviceMemory = not available
hardwareConcurrency = 6
screenResolution = 3008,1692
availableScreenResolution = 3008,1661
timezoneOffset = 240
timezone = America/New_York
sessionStorage = true
localStorage = true
indexedDb = true
addBehavior = false
openDatabase = false
cpuClass = not available
platform = Linux x86_64
plugins = 
canvas = canvas winding:yes,canvas
fp:data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAB9AAAADICAYAAACwGnoBAAAgA
webgl =
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAACWCAYAAABkW7XSAAARcklEQVR4nO3c/2vbi37f8eefsR82uD
webglVendorAndRenderer = VMware, Inc.~SVGA3D; build: RELEASE;  LLVM;
adBlock = false
hasLiedLanguages = false
hasLiedResolution = false
hasLiedOs = false
hasLiedBrowser = false
touchSupport = 0,false,false
fonts = Arial,Arial Narrow,Bitstream Vera Sans Mono,Bookman Old Style,Century
Schoolbook,Courier,Courier New
audio = 35.73833402246237
```

