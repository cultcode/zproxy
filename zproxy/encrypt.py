#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import sys, time
from Crypto.Cipher import DES3
import base64

 
class myDes3Cipher:
  def __init__(self, key, iv, mode):
    self.key = key
    self.iv = iv
    self.mode = mode
    
  def myAddPad(self, raw):
    n = len(raw)
    m = n//8
    y = n%8
    if(y):
      raw = raw.ljust(8*(m+1), chr(8-y))
    else:
      raw = raw.ljust(8*(m+1), chr(8))
    return raw

  def myDelPad(self, raw):
    n = len(raw)
    if n:
      raw = raw.strip(raw[n-1])
    else:
      raw = ''
    return raw
      
      
  def myEncrypt(self, raw):
    raw = self.myAddPad(raw)
    cipher = DES3.new(self.key, self.mode, self.iv)
    data = cipher.encrypt(raw)
    msg = base64.b64encode(data)
    return msg
  
  def myDecrypt(self, raw):
    b64 = base64.b64decode(raw)
    cipher = DES3.new(self.key, self.mode, self.iv)
    msg = cipher.decrypt(b64) 
    msg = self.myDelPad(msg)   
    return msg
    
if __name__ == '__main__':
  import getopt

  myDes3Key = 'D^=^vGfAdUTixobQP$HhsTsa'
  myDes3Iv = 'aVtsvC#S'
  myDes3 = myDes3Cipher(myDes3Key, myDes3Iv, DES3.MODE_CBC)

  isencrypt = False
  data = None

  shortopts = 'ed:'
  try:
    optlist, args = getopt.getopt(sys.argv[1:], shortopts)
    for key, value in optlist:
      if key == '-e':
        isencrypt = True
      elif key == '-d':
        data = value
  except getopt.GetoptError as e:
    print(e, file=sys.stderr)
    sys.exit(2)

  if not data:
    print("ERROR:-d must be specified with data")
    sys.exit(2)
  else:
    if isencrypt:
      data = myDes3.myEncrypt(data)
    else:
      data = myDes3.myDecrypt(data)

  print(data)

