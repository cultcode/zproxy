#!/bin/sh
while true; do if ! pgrep -f deliMastSvr.py; then date; curl -sS -X POST 127.0.0.1:7070/ZkAgentSvr/DeliMastSvr/ReleaseToken; echo; fi; sleep 30; done
