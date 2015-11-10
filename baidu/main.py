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
    if tieba == 1:
        print 'Start Tieba Signin..........'
        for temp in tieba:
            b.sign_in(temp)
        print 'Tieba Done'
    else:
        print 'No Tieba'

    if wenku == 1:
        print 'Start Wenku Signin..........'
        b.wenku_get_docid()
        b.wenku_signin()
        print 'Wenku Done'
    else:
        print 'No Wenku'

if __name__ == '__main__':
    main()
    raw_input('PRESS ENTER TO EXIT!!')