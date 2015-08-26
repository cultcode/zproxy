#!/bin/sh
pkill -f monitor_deli.sh
pkill -f zproxy
sleep 3
nohup /home/Titan/zproxy/zproxy.sh >& /home/Titan/zproxy/zproxy.sh.log &
nohup /home/Titan/zproxy/monitor_deli.sh >& /home/Titan/zproxy/monitor_deli.sh.log &
pgrep -lf zproxy
pgrep -lf monitor_deli.sh
