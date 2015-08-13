#!/bin/sh
while true; do if ! pgrep -f deliMastSvr.py; then date; curl -sS -X POST 127.0.0.1:7070/ZkAgentSvr/ReleaseDeliMaster; echo; fi; sleep 1; done
