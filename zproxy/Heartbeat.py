#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

from threading import Thread, Event
from zproxy import zclient
import logging

class Heartbeat(Thread):
  def __init__(self, event):
    Thread.__init__(self)
    self.beat = event

  def run(self):
    while True:
      if(self.beat.wait(60)):
        pass
      else:
        # call a function
        logging.error("Heatbeat stopped for 60s, switch deli master")
        identity = 'deli'
        ret=zclient.remove_owned_node('/'+identity+'/barrier')
