#!/bin/sh
pkill -f zproxy
pkill -f monitor_deli.sh
nohup /home/Titan/zproxy/zproxy.sh >& /home/Titan/zproxy/zproxy.sh.log &
nohup /home/Titan/zproxy/monitor_deli.sh >& /home/Titan/zproxy/monitor_deli.sh.log &
pgrep -lf zproxy
pgrep -lf monitor_deli.sh
