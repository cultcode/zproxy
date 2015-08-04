#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

from bottle import route, run, post, request
from Crypto.Cipher import DES3
import json
import logging
from zproxy import encrypt, zclient, shell

myDes3Key = ''
myDes3Iv = ''
myDes3 = None

@route('/hello')
def hello():
  return "Hello World!"

@post('/ZkAgentSvr/GetDeliMaster')
def GetLowestP2P():
  content = request.body.read()
  if content:
    if shell.config['encrypt']:
      content = myDes3.myDecrypt(content)

  logging.info('Received '+content)

  if content:
    decodejson = json.loads(content, encoding='UTF-8')
    #print decodejson['EpochTime']

  master = zclient.query_barrier('p2p')
  #{"Status":1,"StatusDesc":"success","NodeId":1}
  if master is not None:
    content = {"Status":1,"StatusDesc":"success","NodeId":master}
  else:
    content = {"Status":0,"StatusDesc":"failure","NodeId":0}
  content = json.dumps(content)

  logging.info('Sent     '+content)

  if shell.config['encrypt']:
    content = myDes3.myEncrypt(content)

  return content

@post('/ZkAgentSvr/PayloadReport')
def PayloadReport():
  return
    
  
def start():
  global myDes3Key, myDes3Iv, myDes3
  myDes3Key = shell.config['des3-key']
  myDes3Iv = shell.config['des3-iv']
  myDes3 = encrypt.myDes3Cipher(myDes3Key, myDes3Iv, DES3.MODE_CBC)

  run(host=shell.config['local_address'], port=shell.config['local_port'], debug=True)
