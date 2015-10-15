#!/bin/sh
#pkill -f monitor_deli.sh
pkill -f zproxy.sh
pkill -f zproxy.py
nohup /home/Titan/zproxy/zproxy.sh >> /home/Titan/zproxy/zproxy.sh.log 2>&1 &
#nohup /home/Titan/zproxy/monitor_deli.sh >> /home/Titan/zproxy/monitor_deli.sh.log 2>&1 &
sleep 3
pgrep -lf zproxy
