import requests
import sys
from requests.adapters import HTTPAdapter
import os
from threading import Thread
import threading
from datetime import datetime

requests.packages.urllib3.disable_warnings()
#requests.adapters.DEFAULT_RETRIES = 1000000

threads = []

d1 = []
d2 = []

dirno = []

def banner():
    banner = '''\033[1;32m
__        __   _     ____ ___ ______     __
\ \      / /__| |__ |  _ \_ _|  _ \ \   / /__ _ __   ___  _ __ ___  
 \ \ /\ / / _ \ '_ \| | | | || |_) \ \ / / _ \ '_ \ / _ \| '_ ` _ \ 
  \ V  V /  __/ |_) | |_| | ||  _ < \ V /  __/ | | | (_) | | | | | |
   \_/\_/ \___|_.__/|____/___|_| \_\ \_/ \___|_| |_|\___/|_| |_| |_|
    \033[1;m
Fast Web Directory Scanner
Designed by M4TRIX_H4CK3R

\033[1;34mFacebook\033[1;m: https://www.facebook.com/aggarwalhacker
\033[1;34mTwitter\033[1;m: https://twitter.com/SurajAg001
\033[1;34mGithub\033[1;m: https://github.com/matrixhacker0001
    '''
    print(banner)

def helpBanner():
    print("Usage: python nmap.py [URL] [COOKIES]")
    print("\nURL: Url of the site")
    print("COOKIES: Cookie to be used {OPTIONAL}")

def main(url):
    banner()
    if "http" in url:
        scan(url)
    else:
        url = "http://" + url
        scan(url)

def dirScan(url, text):
    print("\n\033[1;32m[+]  Directories for:\033[1;m {}".format(text))
    print("======================" + "=" * len(text) + "=")
    createList(url + "/")

def subbrute(url, f):
  for i in range(0,10):
    t = Thread(target=bruteDir, args=(url, f))
    t.start()
    threads.append(t)

def bruteDir(url, start, end, lines):
	for l in range(start, end):
   		r = requests.get(url + lines[l].rstrip("\n") + "/", allow_redirects=False, verify=False)
   		sys.stdout.write("\x1b[2K[ {} ] ==> {} \r".format(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), r.url))
   		sys.stdout.flush()
	    	if 0 < r.status_code < 400:
        	    print("\x1b[2K\033[1;34m[*]\033[1;m {} [ Code: {} ]".format(r.url, r.status_code))
        	    dirno.append("0")
        	    if ".txt" in r.url:
        	    	continue
        	    else:
        	    	d1.append(r.url)

def createList(url):
    f = open(os.path.dirname(os.path.abspath(sys.argv[0])) + "/common.txt", "r")
    lines = f.readlines()
    sran = len(lines) / 350
    print("\x1b[2K\n---- Scanning Directory : {} ----\r".format(url))
    threads[:] = []
    for i in range(0,350):
    	#print(str(i) + ". " + str(i * sran) + " : " + str((i + 1) * sran) + " : " + str(len(lines) - ((i + 1) * sran)))
    	t = Thread(target=bruteDir, args=(url, i * sran, (i + 1) * sran, lines))
    	t.start()
    	threads.append(t)
    if (len(lines) - (350 * sran)) > 0:
    	#print(str(100) + ". " + str(100 * sran) + " : " + str(len(lines)) + " : " + str(len(lines) - ((100 + 1) * sran)))
    	global t2
    	t2 = Thread(target=bruteDir, args=(url, 350 * sran, len(lines), lines))
    	t2.start()
    while t2.isAlive():
    	continue
    check()

def transfer():
	if len(d1) > 0:
		for i in range(0,len(d1)):
	    		d2.append(d1[0])
    			d1.remove(d1[0])

def check():
	if len(d1) > 0 or len(d2) > 0:
		transfer()
		url = d2[0]
		d2.remove(url)
		createList(url)

def scan(url):
    try:
    	r = requests.get(url, allow_redirects=False, verify=False)
    	print("\033[1;32mURL:\033[1;m {}".format(r.url))
    	print("\033[1;32mCODE:\033[1;m {}".format(r.status_code))
    	start = datetime.now()
    	dirScan(url, r.url)
    	end = datetime.now()
    	print("\x1b[2K\n\033[1;33mNumber of Directories Found:\033[1;m {}".format(len(dirno)))
    	print("\033[1;34mStart Time:\033[1;m {}".format(start))
    	print("\033[1;34mEnd Time:\033[1;m {}".format(end))
    	print("\033[1;34mScan Time:\033[1;m {}".format(end - start))
    	print("\nFinished..!!")
    except requests.exceptions.RequestException as e:
    	print(e)
    	sys.exit(1)

try:
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        helpBanner()
    else:
        main(sys.argv[1])
except KeyboardInterrupt:
    print("\nUser Interrupted..!  Exiting..!!")
