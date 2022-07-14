'''
Setup script for HTTP server for 2D sound map prototype for user evaluation
Default port: 8000
Default browser: Safari
'''

import sys
import time
import threading
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import subprocess

# Get filepaths
path_abs = os.path.abspath(__file__)
dname = os.path.join(os.path.dirname(path_abs), 'sound-map-visualizer')
os.chdir(dname)

ip   = 'localhost'
port = 8000
url  = f'http://{ip}:{port}'

# Server handler
def start_server():
    print("Starting server..")
    address = (ip, port)
    httpd   = HTTPServer(address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

threading.Thread(target=start_server).start()
cmd = "osascript -e " + "'get version of application " +  '"Safari"' + "'"

# Check browser version and default browser
version = subprocess.check_output(cmd, shell=True).strip().decode('utf-8')
controller = webbrowser.get('safari')
command = "x=~/Library/Preferences/com.apple.LaunchServices/com.apple.launchservices.secure.plist; \
plutil -convert xml1 $x; \
grep 'https' -b3 $x | awk 'NR==2 {split($2, arr, \"[><]\"); print arr[3]}'; \
plutil -convert binary1 $x"
default_browser = subprocess.check_output(command, shell=True).strip().decode('utf-8')

# Check browser settings
if (version == '15.4'):
    controller.open_new(url)
elif (version != '15.4' or default_browser != 'com.apple.safari'):
    webbrowser.open_new(url)
else:
    try:
        webbrowser.get('chrome').open_new(url)
    except:
        print('Your Safari version is too old or you do not have Chrome installed. Open another browser on {url}'.format(url=url))

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)

