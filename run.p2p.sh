#!/bin/sh
pkill -f monitor_p2p.sh
pkill -f zproxy.sh
pkill -f zproxy.py
sleep 3
nohup /home/Titan/zproxy/zproxy.sh >> /home/Titan/zproxy/zproxy.sh.log 2>&1 &
nohup /home/Titan/zproxy/monitor_p2p.sh >> /home/Titan/zproxy/monitor_p2p.sh.log 2>&1 &
pgrep -lf zproxy
