#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        m = n/8
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
        
    
