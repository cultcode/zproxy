#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import logging
import json
import sys
import time

from kazoo.client import KazooClient
from kazoo.protocol.states import *
from kazoo.exceptions import *

from zproxy import shell

zk = None


def create_barrier():
  path_barrier = '/'+shell.config['identity']+'/barrier'
  value_barrier = json.dumps({'NodeId':shell.config['nodeid']}, encoding='utf-8')
  if path_barrier is not None:
    try:
      zk.create(path_barrier, value=value_barrier, acl=None, ephemeral=True, sequence=False, makepath=True)
    except NodeExistsError as e:
      pass
    except:
      logging.error(e)
      sys.exit(1)


def my_listener(state):
    logging.info("Connection Event "+state)
    # Register somewhere that the session was lost
    if state == KazooState.LOST:
      pass
    # Handle being disconnected from Zookeeper
    elif state == KazooState.SUSPENDED:
      pass
    # Handle being connected/reconnected to Zookeeper
    else:
      zk.handler.spawn(create_barrier)


def start():
  global zk

  zk = KazooClient()

  if shell.config['barrier'] is True:
    path_barrier = '/'+shell.config['identity']+'/barrier'
    value_barrier = json.dumps({'NodeId':shell.config['nodeid']}, encoding='utf-8')

    @zk.DataWatch(path_barrier)
    def watch_node(data, stat, event):
      if event:
        logging.info("Node Event %s %s" %(event.path, event.type))
        if event.type == EventType.DELETED:
          zk.handler.spawn(create_barrier)
      

  zk.add_listener(my_listener)

  zk.start()

  while True:
    time.sleep(5)
