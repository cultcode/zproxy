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


def get_version():
  version = ''
  try:
    import pkg_resources
    version = pkg_resources.get_distribution('zproxy').version
  except Exception as e:
    #pass
    print("warning: zproxy not installed yet and version is unknown")
    version = "0.0"
  return version


def get_epochtime():
  import time
  return hex(int(time.time()))[2:]


def get_hostname():
  import socket
  return socket.gethostname()

