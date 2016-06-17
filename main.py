#coding:utf-8

import baidu
import ConfigParser

def main():
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    username = cf.get('INFO','username')
    password = cf.get('INFO','password')
    tieba = int(cf.get('INFO','tieba'))
    wenku = int(cf.get('INFO','wenku'))

    b = baidu.Baidu(username,password)
    b.login()
    add_ed2klink()

def add_ed2klink():
    ed2k_link = raw_input('paste ed2k link here:')
    yun = baidu.BaiduYun()
    yun.add_offline(ed2k_link)


if __name__ == '__main__':
    main()
    raw_input('PRESS ENTER TO EXIT!!')