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
def GetDeliMaster():
  content_r = {'Status':0,'StatusDesc':'Success'}
  identity = None

  content = request.body.read()
  if content:
    if shell.config['encrypt']:
      content = myDes3.myDecrypt(content)

  logging.info('Received '+content)

  if not content:
    #HACK
    #content_r['StatusDesc'] = 'Request body is empty'
    identity = 'deli'
  else:
    try:
      decodejson = json.loads(content, encoding='UTF-8')
    except:
      content_r['StatusDesc'] = 'Json parsing failed'
    else:
      #HACK
      #identity = decodejson.get('Identity',None)
      identity = decodejson.get('Identity','deli')

  if not identity:
    content_r['StatusDesc'] = 'No Identity specified'
  else:
    ret = zclient.query_owned_node('/'+identity+'/barrier')

    if ret[1]:
      content_r['StatusDesc'] = ret[1]
    elif ret[0] != shell.config['nodeid']:
      content_r['StatusDesc'] = 'Master is NodeId %d' %ret[0]
    else:
      content_r['Status'] = 1

  content_r = json.dumps(content_r)

  logging.info('Sent     '+content_r)

  if shell.config['encrypt']:
    content_r = myDes3.myEncrypt(content_r)

  return content_r


@post('/ZkAgentSvr/ReleaseDeliMaster')
def RealseDeliMaster():
  content_r = {'Status':0,'StatusDesc':'Success'}
  identity = None

  content = request.body.read()
  logging.info('Received '+content)

  if not content:
    #HACK
    #content_r['StatusDesc'] = 'Request body is empty'
    identity = 'deli'
  else:
    try:
      decodejson = json.loads(content, encoding='UTF-8')
    except:
      content_r['StatusDesc'] = 'Json parsing failed'
    else:
      #HACK
      #identity = decodejson.get('Identity',None)
      identity = decodejson.get('Identity','deli')

  if not identity:
    content_r['StatusDesc'] = 'No Identity specified'
  else:
    ret=zclient.remove_owned_node('/'+identity+'/barrier')

    if ret:
      content_r['StatusDesc'] = ret
    else:
      content_r['Status'] = 1

  content_r = json.dumps(content_r)

  logging.info('Sent     '+content_r)

  return content_r


@post('/ZkAgentSvr/PayloadReport')
def PayloadReport():
  content_r = {'Status':0,'StatusDesc':'Success'}
  identity = None

  content = request.body.read()
  if content:
    if shell.config['encrypt']:
      content = myDes3.myDecrypt(content)

  logging.info('Received '+content)

  if not content:
    content_r['StatusDesc'] = 'Request body is empty'
  else:
    try:
      decodejson = json.loads(content, encoding='UTF-8')
    except:
      content_r['StatusDesc'] = 'Json parsing failed'
    else:
      #HACK
      #identity = decodejson.pop('Identity',None)
      identity = decodejson.pop('Identity','p2p')
      payload  = decodejson

  if not identity:
    content_r['StatusDesc'] = 'No Identity specified'
  elif not payload:
    content_r['StatusDesc'] = 'No TaskSum specified'
  else:
    ret = zclient.update_owned_childnode('/'+identity, payload)

    if ret:
      content_r['StatusDesc'] = ret
    else:
      content_r['Status'] = 0

  content_r = json.dumps(content_r)

  logging.info('Sent     '+content_r)

  if shell.config['encrypt']:
    content_r = myDes3.myEncrypt(content_r)

  return content_r


@post('/ZkAgentSvr/GetLowestP2P')
def GetLowestP2P():
  content_r = {'Status':0,'StatusDesc':'Success','NodeId':0}
  identity = None

  content = request.body.read()
  if content:
    if shell.config['encrypt']:
      content = myDes3.myDecrypt(content)

  logging.info('Received '+content)

  if not content:
    #HACK
    #content_r['StatusDesc'] = 'Request body is empty'
    identity = 'p2p'
  else:
    try:
      decodejson = json.loads(content, encoding='UTF-8')
    except:
      content_r['StatusDesc'] = 'Json parsing failed'
    else:
      #HACK
      #identity = decodejson.get('Identity',None)
      identity = decodejson.get('Identity','p2p')

  if not identity:
    content_r['StatusDesc'] = 'No Identity specified'
  else:
    ret = zclient.query_lowest_childnode('/'+identity)

    if ret[1]:
      content_r['StatusDesc'] = ret[1]
    else:
      content_r['Status'] = 1
      content_r['NodeId'] = ret[0]

  content_r = json.dumps(content_r)

  logging.info('Sent     '+content_r)

  if shell.config['encrypt']:
    content_r = myDes3.myEncrypt(content_r)

  return content_r

@post('/ZkAgentSvr/Monitor')
def Monitor():
  content_r = {'Status':0,'StatusDesc':'Success','tree':{}}
  try:
    ret = zclient.export_tree('/')
  except Exception as e:
    content_r['StatusDesc'] = "Exception emerged in exporting tree: %s" %e
  else:
    content_r['Status'] = 1
    content_r['tree'] = ret

  content_r = json.dumps(content_r)
  return content_r


def start():
  global myDes3Key, myDes3Iv, myDes3
  myDes3Key = shell.config['des3-key']
  myDes3Iv = shell.config['des3-iv']
  myDes3 = encrypt.myDes3Cipher(myDes3Key, myDes3Iv, DES3.MODE_CBC)

  run(host=shell.config['local_address'], port=shell.config['local_port'], debug=True)
