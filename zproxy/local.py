#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

from bottle import route, run, post, request
from Crypto.Cipher import DES3
import json
import logging
from zproxy import encrypt

myDes3Key = ''
myDes3Iv = ''
myDes3 = None

@route('/hello')
def hello():
  return "Hello World!"

@post('/test') # or @route('/test', method='POST')
def test():
  content = request.body.read()
  logging.info('Received'+content)
  #content = myDes3.myEncrypt(content)
  content = myDes3.myDecrypt(content)
  decodejson = json.loads(content, encoding='UTF-8')
  #print decodejson['EpochTime']
  return decodejson

def start(config):
  global myDes3Key, myDes3Iv, myDes3
  myDes3Key = config['des3-key']
  myDes3Iv = config['des3-iv']
  myDes3 = encrypt.myDes3Cipher(myDes3Key, myDes3Iv, DES3.MODE_CBC)

  run(host=config['local_address'], port=config['local_port'], debug=True)
