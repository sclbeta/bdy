#-*-coding:utf-8-*-
import urllib
import urllib2
import execjs
import re
import cookielib
from bs4 import BeautifulSoup
import json
import time
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

class baiduyun():
	