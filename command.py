import os
import sys
import time
import telnetlib

IP=(sys.argv[1])
COMMAND=str((sys.argv[2]))
print(COMMAND)

def vg(*args):
    user = 'service'
    password = 'billing'
    tn = telnetlib.Telnet(IP)
    tn.write(user + '\n')
    tn.write(password + '\n')
    tn.write('disable clipaging\n')
    tn.write(COMMAND + '\n')
    time.sleep(25)
    all_result = tn.read_very_eager().decode('utf-8')
    print(all_result)


vg(IP,COMMAND)

