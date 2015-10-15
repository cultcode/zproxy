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
    timeout = 60
    while True:
      self.beat.wait(timeout)

      ret = self.beat.isSet()

      if ret:
        self.beat.clear()
      else:
        # call a function
        logging.error("Heatbeat stopped for %d seconds, switch deli master" %timeout)
        identity = 'deli'
        desc=zclient.remove_owned_node('/'+identity+'/barrier')
        logging.info(desc)

