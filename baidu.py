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

class Baidu(object):

    def __init__(self,user,pwd):
        self.usr = user
        self.pwd = pwd

    def login(self, v_code='', c_string=''):
        #print 'b'
        self.get_pre_login_info()
        url = 'https://passport.baidu.com/v2/api/?login'
        '''
        head = {
            "Origin": "https://passport.baidu.com",
            "Accept-Encoding": "gzip, deflate",
            "Host": "passport.baidu.com",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Cache-Control": "max-age=0",
            "Referer": "https://passport.baidu.com/v2/?login",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36"
        }
        '''
        data = {
            "staticpage": "https://passport.baidu.com/static/passpc-account/html/v3Jump.html",
            "charset": "UTF-8",
            "token": self.token,
            "tpl": "pp",
            "subpro": "",
            "apiver": "v3",
            "tt": execjs.eval('new Date().getTime()'),
            "codestring": c_string,
            "safeflg": "0",
            "u": "https://passport.baidu.com/",
            "isPhone": "false",
            "detect": "1",
            "quick_user": "0",
            "logintype": "basicLogin",
            "logLoginType": "pc_loginBasic",
            "idc": "",
            "loginmerge": "true",
            "username": self.usr,
            "password": self.rsa_pwd,
            "verifycode": v_code,
            "mem_pass": "on",
            "rsakey": self.key,
            "crypttype": "12",
            "ppui_logintime": execjs.eval('20000 + 10000 * Math.random() % 10000'),
            "gid": self.create_gid(),
            "callback": "parent.bd__pcbs__dvpmkh"
        }
        data = urllib.urlencode(data)
        #print data
        req = urllib2.Request(url, data)
        # req.add_header(head)
        res = urllib2.urlopen(req).read()
        if 'err_no=257' in res:
            print 'fail'
            #pass
            self.check_vcode(res)
        elif 'err_no=0' in res:
            print 'success'
            return True
        else:
            print 'fail1'
            pass

    def create_gid(self):
        temp = execjs.compile('''function create_gid() {
            return "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,
                function(c) {var r = Math.random() * 16 | 0,v = c == "x" ? r : (r & 3 | 8);
                    return v.toString(16);})}''')
        self.gid = temp.call('create_gid')
        return self.gid

    def get_pre_login_info(self):
        url = 'https://passport.baidu.com/center'
        urllib2.urlopen(url)
        url = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&' +  str(int(time.time()) * 1000) + '&class=login&logintype=basicLogin&callback=bd__cbs__hqe0c'
        content = urllib2.urlopen(url).read()
        content = content[len('bd__cbs__hqe0c('):-1]
        content = execjs.eval(content)
        self.token = content['data']['token']

        url = 'https://passport.baidu.com/v2/getpublickey?token=' + self.token + \
            '&tpl=pp&apiver=v3&tt=' + \
            str(int(time.time()) * 1000) + '&callback=bd__cbs__zgtpei'
        content = urllib2.urlopen(url).read()
        content = content[len('bd__cbs__zgtpei('):-1]
        content = execjs.eval(content)
        pubkey_temp = content['pubkey']
        self.pubkey = pubkey_temp  # .replace('\n','\\n')
        self.key = content['key']
        # print self.token, self.pubkey, self.key
        self.encrypt_keys()

    def encrypt_keys(self):
        f = file('baidujiami.js', 'r')
        content = f.read().decode('utf8')
        ctx = execjs.compile(content)
        self.rsa_pwd = ctx.call('any_rsa_pass', self.pubkey, self.pwd)
        f.close()

    def check_login(self):
        url = 'http://www.baidu.com'
        res = urllib2.urlopen(url).read()
        #print res

    def check_vcode(self, res):
        codestring = re.search('codeString=.+&userName?', res)
        if codestring:
            codestring = codestring.group()
            print 'https://passport.baidu.com/cgi-bin/genimage?' + codestring[11:-9]
            v_code = raw_input('input the v_code:')
            url = 'https://passport.baidu.com/v2/?checkvcode&token='+self.token+'&tpl=pp&apiver=v3&tt='+str(execjs.eval('new Date().getTime()'))+'&verifycode='+v_code+'&codestring='+codestring[11:-9]+'&callback=bd__cbs__7nsuuj'
            sth = urllib2.urlopen(url).read()
            print sth
            self.login(v_code, codestring[11:-9])
        else:
            print 'none'

    def sign_in(self,tieba):
        #print tieba
        self.tieba = tieba
        tieba = tieba.encode('gb2312')
        self.tieba_gbk = urllib.quote(tieba)
        #print self.tieba,self.tieba_gbk,tieba        
        url = 'http://tieba.baidu.com/sign/add'
        data = {
            'ie':'utf-8',
            'kw':self.tieba,
            'tbs':self.get_tbs()
        }
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
        res = urllib2.urlopen(req).read()
        if 'success' in res:
            print self.tieba,' Success'

class BaiduYun(object):
    """docstring for baiduyun"""
    def __init__(self):
        super(BaiduYun, self).__init__()
    
    def add_offline(self,ed2k_link):
        url = 'http://pan.baidu.com/rest/2.0/services/cloud_dl?bdstoken=dea672296602d8fe48b7dca76e5b34a6&channel=chunlei&web=1&app_id=250528&logid=MTQ2NTgyNjEwMzA1ODAuMjUxMDkyODI2NDY1NTc4MDc=&clienttype=0'
        data = {
            'app_id':'250528',
            'method':'add_task',
            'save_path':'/autooffline/',
            'source_url':ed2k_link,
            'type':'3'
        }
        data = urllib.urlencode(data)
        #print data
        req = urllib2.Request(url, data)
        # req.add_header(head)
        res = urllib2.urlopen(req).read()
        print res

    def get_dlink(self):
        t = execjs.eval('new Date().getTime()')
        url = 'https://d.pcs.baidu.com/rest/2.0/pcs/manage?method=listhost&t='+ t +'&callback=jQuery17207657948233440389_1466165739106&_=' + str(int(t)+3)
        res = urllib2.urlopen(url).read()
        print res
        get_dlink1()
    def get_dlink1(self):
        t = int(time.time())
        url = 'http://pan.baidu.com/api/download?sign=cAN4FH2O7%2FRT7MQ5i5%2FzrybZ6Wz8fMKNY1ItaZ815hRKBXYJ%2FF6xYg%3D%3D&timestamp=' + str(t) + '&fidlist=%5B893131684120802%5D&type=dlink&bdstoken=dea672296602d8fe48b7dca76e5b34a6&channel=chunlei&web=1&app_id=250528&logid=MTQ2NjE2NjEwMDEyODAuMjc0MDE1Njk3ODkyMDc4OQ==&clienttype=0'
        res = urllib2.urlopen(url).read()
        print res
        get_dlink2()
    def get_dlink2(self):
        pass