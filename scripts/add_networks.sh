#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
route del default gw 172.1.2.1
ip route add 10.5.1.0/24 via 172.1.2.1 dev ens192
