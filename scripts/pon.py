import os
import sys
import time
import re
import telnetlib

host = '10.5.1.2'

user = 'service'
password = 'billing'


try:
    ONU=(sys.argv[1])
    VLAN=(sys.argv[2])
except:
    pass

def fun():

    try:
        tn = telnetlib.Telnet(host)
        tn.write(user + '\r\n')
        tn.write(password + '\r\n')
        tn.write('enable\r\n')
        tn.write('config\r\n')
        tn.write('vty output show-all\r\n')
        tn.write('interface epon 0/0\r\n')
        tn.write('ont modify 1' + ' ' + ONU + ' ' + 'ont-srvprofile-id ' + ' ' + VLAN + '\r\n')
        time.sleep(1)
        r4 = tn.read_very_eager().split('OLT')[6]
        print(r4)
        tn.close()
    except :
        pass

fun()


