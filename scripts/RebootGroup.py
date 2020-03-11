import os
import sys
import time
import re
import telnetlib
import pymysql.cursors
import pymysql

user = '***'
password = '***'


try:
    GROUP=(sys.argv[1])
except:
    pass


def db():
    conn = ( pymysql.connect(host = '***',
                             user = '***',
                             password = '***',
                             database = '***',
                             charset='utf8' ) )

    cursor = conn.cursor()
    cursor.execute('SELECT equipment.ip FROM equipment WHERE equipment.`group` = %s',(GROUP))

    user = '***'
    password = '***'
    for data in cursor:
        host = ''.join(data)
        tn = telnetlib.Telnet(host)

        tn.write(user + '\n')
        tn.write(password + '\n')

        tn.write('reboot force_agree\n')
db()


