#coding:utf-8

import baidu
import ConfigParser

def main():
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    username = cf.get('INFO','username')
    password = cf.get('INFO','password')
    tieba = cf.get('INFO','tieba').split('|')
    wenku = int(cf.get('INFO','wenku'))

    b = baidu.Baidu(username,password)
    b.login()
    if tieba:
        for temp in tieba:
            b.sign_in(temp)

    if wenku == 1:
        pass

if __name__ == '__main__':
    main()