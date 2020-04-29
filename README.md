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
http://172.17.0.2/
http://172.17.0.2/TwYCEvgMHs
http://kali.local/
http://kali.local/TwYCEvgMHs

[+] Available payloads:
http://172.17.0.2/lin_x64_https.bin
http://172.17.0.2/lin_x86_https.bin
http://172.17.0.2/win_x64_https.dll
http://172.17.0.2/win_x64_https.exe
http://172.17.0.2/win_x64_https.ps1
http://172.17.0.2/win_x64_tcp.exe
http://172.17.0.2/win_x86_https.dll
http://172.17.0.2/win_x86_https.exe
http://172.17.0.2/win_x86_https.ps1
http://kali.local/lin_x64_https.bin
http://kali.local/lin_x86_https.bin
http://kali.local/win_x64_https.dll
http://kali.local/win_x64_https.exe
http://kali.local/win_x64_https.ps1
http://kali.local/win_x64_tcp.exe
http://kali.local/win_x86_https.dll
http://kali.local/win_x86_https.exe
http://kali.local/win_x86_https.ps1

[+] Now all files in the 'payloads' directory and fingerprint server on port 8000
```

# Fingerprinting
Uses [JS Fingerprint 2](https://github.com/Valve/fingerprintjs2) and stores output in `logs/<client IP>.txt`

