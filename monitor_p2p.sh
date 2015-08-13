#!/bin/sh
while true; do if ! pgrep -lf P2POrgSvr.exe; then curl -X POST 127.0.0.1:7070/ZkAgentSvr/PayloadReport -d '{"TaskSum":9223372036854775807}'; fi; sleep 1; done
