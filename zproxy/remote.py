#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import sys
import requests
from Crypto.Cipher import DES3
import json
import logging
from zproxy import encrypt, common

myDes3Key = ''
myDes3Iv = ''
myDes3 = None

def svr_init(config):
  global myDes3Key, myDes3Iv, myDes3
  myDes3Key = config['des3-key']
  myDes3Iv = config['des3-iv']
  myDes3 = encrypt.myDes3Cipher(myDes3Key, myDes3Iv, DES3.MODE_CBC)

  payload = {'EpochTime':common.get_epochtime(),'NodeName':common.get_hostname(),'Version':common.get_version(),"SvrType":15}
  #payload = {'EpochTime':common.get_epochtime(),'NodeName':'CSDX-TintanCDN.15-143','Version':common.get_version(),"SvrType":15}
  payload = json.dumps(payload, encoding='UTF-8')
  logging.info('Sent:     '+payload)
  payload = myDes3.myEncrypt(payload)
  r = requests.post(config['dbagent']+'/DBAgentSvr/SvrInit', data=payload)

  r.raise_for_status()

  content = myDes3.myDecrypt(r.text)
  logging.info('Received: '+content)
  decodejson = json.loads(content, encoding='UTF-8')

  if decodejson['Status'] == 0:
    logging.error('Failure status returned')
    sys.exit(1)
  elif decodejson['Status'] == 1:
    config['nodeid'] = decodejson['NodeId']
  else:
    logging.error('Unknown status returned')
    sys.exit(1)

  return
