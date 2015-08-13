#!/bin/sh
while true; do if ! pgrep -f deliMastSvr.py; then curl -X POST 127.0.0.1:7070/ZkAgentSvr/ReleaseDeliMaster; fi; sleep 1; done
