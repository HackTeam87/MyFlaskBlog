#-*- coding: utf-8 -*-
import os
import sys
import telnetlib
import time

sw = ['10.1.1.11']


def db():
    user = 'service'
    password = 'billing'
    for data in sw:
        host = ''.join(data)
        tn = telnetlib.Telnet(host)

        tn.write(user + '\n')
        tn.write(password + '\n')
        tn.write('disable clipaging\n')      
        tn.write('show switch\n')
        time.sleep(1)

        all_result = tn.read_very_eager().decode('utf-8')
        print(all_result)
db()



