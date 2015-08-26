#!/bin/sh
pkill -f monitor_p2p.sh
pkill -f zproxy
sleep 3
nohup /home/Titan/zproxy/zproxy.sh >& /home/Titan/zproxy/zproxy.sh.log &
nohup /home/Titan/zproxy/monitor_p2p.sh >& /home/Titan/zproxy/monitor_p2p.sh.log &
pgrep -lf zproxy
pgrep -lf monitor_p2p.sh
