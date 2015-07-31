#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
  with_statement

import os
import sys


def compat_ord(s):
  if type(s) == int:
    return s
  return _ord(s)


def compat_chr(d):
  if bytes == str:
    return _chr(d)
  return bytes([d])


_ord = ord
_chr = chr
ord = compat_ord
chr = compat_chr


def to_bytes(s):
  if bytes != str:
    if type(s) == str:
      return s.encode('utf-8')
  return s


def to_str(s):
  if bytes != str:
    if type(s) == bytes:
      return s.decode('utf-8')
  return s


def getVersion():
  version = ''
  try:
    import pkg_resources
    version = pkg_resources.get_distribution('zproxy').version
  except Exception as e:
    #pass
    print_exception(e)
    sys.exit(1)
  return version


def getEpochTime():
  import time
  return hex(int(time.time()))[2:]


def getHostName():
  import socket
  return socket.gethostname()

