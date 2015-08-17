#!/bin/sh
while true; do if ! pgrep -f P2POrgSvr.exe; then date; curl -sS -X POST 127.0.0.1:7070/ZkAgentSvr/P2POrgSvr/PayloadReport -d '{"TaskSum":9223372036854775807}'; echo; fi; sleep 1; done
