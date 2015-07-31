#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

from kazoo.client import KazooClient
from kazoo.protocol.states import *
from kazoo.exceptions import *

import logging
import json
import sys
import time

zk = None
path_barrier = None
value_barrier = None

def create_barrier():
  if path_barrier is not None:
    try:
      logging.info('create_barrier')
      zk.create(path_barrier, value=value_barrier, acl=None, ephemeral=True, sequence=False, makepath=True)
    except NodeExistsError:
      pass
    except:
      logging.error(e)
      sys.exit(1)


def my_listener(state):
    logging.info(state)
    # Register somewhere that the session was lost
    if state == KazooState.LOST:
      pass
    # Handle being disconnected from Zookeeper
    elif state == KazooState.SUSPENDED:
      pass
    # Handle being connected/reconnected to Zookeeper
    else:
      zk.handler.spawn(create_barrier)


def start(config):
  global zk, path_barrier, value_barrier

  zk = KazooClient()

  if config['barrier'] is True:
    path_barrier = '/'+config['identity']+'/barrier'
    value_barrier = json.dumps({'NodeId':config['nodeid']}, encoding='utf-8')

    @zk.DataWatch(path_barrier)
    def watch_node(data, stat):
      if data:
        logging.info("data: %s" % data.decode("utf-8"))
      zk.handler.spawn(create_barrier)
      

  zk.add_listener(my_listener)

  zk.start()

  while True:
    time.sleep(5)
