import os
import sys
import time
import re
import telnetlib

host = '10.5.1.2'
user = '***'
password = '***'

try:
    PORT=(sys.argv[1])
except:
    pass


def optical():

    tn = telnetlib.Telnet(host)
    tn.write(user + '\r\n')
    tn.write(password + '\r\n')
    tn.write('enable\r\n')
    tn.write('config\r\n')
    tn.write('vty output show-all\r\n')
    tn.write('interface epon 0/0\r\n')
    tn.write('show ont optical-info 1 all\r\n')
    time.sleep(1)
    r1 = tn.read_very_eager().split('OLT')[6]
    print(r1)
    tn.close()

    tn = telnetlib.Telnet(host)
    tn.write(user + '\r\n')
    tn.write(password + '\r\n')
    tn.write('enable\r\n')
    tn.write('config\r\n')
    tn.write('vty output show-all\r\n')
    tn.write('interface epon 0/0\r\n')
    tn.write('show ont info 1 all\r\n')
    time.sleep(1)
    r2 = tn.read_very_eager().split('OLT')[6]
    print(r2)
    tn.close()

    tn = telnetlib.Telnet(host)
    tn.write(user + '\r\n')
    tn.write(password + '\r\n')
    tn.write('enable\r\n')
    tn.write('config\r\n')
    tn.write('vty output show-all\r\n')
    tn.write('show mac-address port epon 0/0/1 with-ont-location\r\n')
    time.sleep(1)
    r3 = tn.read_very_eager().split('OLT')[5]
    print(r3)
    tn.close()

optical()


