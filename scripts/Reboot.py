import os
import sys
import telnetlib

IP=(sys.argv[1])

def reboot(*args):
    user = '***'
    password = '***'

    for host in args:
        tn = telnetlib.Telnet(host)

        tn.write(user + '\n')
        tn.write(password + '\n')

        tn.write('reboot force_agree\n')
reboot(IP)

