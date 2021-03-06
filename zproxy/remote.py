#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import sys
import requests
from Crypto.Cipher import DES3
import json
import logging
from zproxy import encrypt, common, shell

myDes3Key = ''
myDes3Iv = ''
myDes3 = None

def svr_init():
  global myDes3Key, myDes3Iv, myDes3
  myDes3Key = shell.config['des3-key']
  myDes3Iv = shell.config['des3-iv']
  myDes3 = encrypt.myDes3Cipher(myDes3Key, myDes3Iv, DES3.MODE_CBC)

  payload = {'EpochTime':common.get_epochtime(),'NodeName':common.get_hostname(),'Version':common.get_version(),"SvrType":15}
  #payload = {'EpochTime':common.get_epochtime(),'NodeName':'CSDX-TintanCDN.15-143','Version':common.get_version(),"SvrType":15}
  payload = json.dumps(payload, encoding='UTF-8')
  logging.info('Sent:     '+payload)
  payload = myDes3.myEncrypt(payload)
  r = requests.post(shell.config['dbagent']+'/DBAgentSvr/SvrInit', data=payload)

  r.raise_for_status()

  content = myDes3.myDecrypt(r.text)
  logging.info('Received: '+content)
  decodejson = json.loads(content, encoding='UTF-8')

  if decodejson['Status'] == 0:
    logging.error('Failure status returned')
    sys.exit(1)
  elif decodejson['Status'] == 1:
    shell.config['nodeid'] = decodejson['NodeId']
  else:
    logging.error('Unknown status returned')
    sys.exit(1)

  return

def send_sms(mobile, content):
  sn = "DXX-WSS-103-05540"
  pwd = "639989"
  content += '[CDN]'
  headers = {'Content-Type': 'application/x-www-form-urlencoded'}

  if mobile:
    payload = 'sn=%s&pwd=%s&mobile=%s&content=%s' %(sn, pwd, mobile, content)
    logging.info('Sent:     '+payload)

    try:
      r = requests.post('http://sdk.entinfo.cn:8060/webservice.asmx/SendSMS', data = payload, headers=headers)

      r.raise_for_status()
    except Exception as e:
      logging.error('SendSMS failed: %s', e)
    else:
      content = r.text
      logging.info('Received: '+content)

