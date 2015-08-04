#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import logging
import json
import sys

from kazoo.client import KazooClient
from kazoo.protocol.states import *
from kazoo.exceptions import *

from zproxy import shell

zk = None
offset = -1


def create_ephemeral():
  if shell.config['barrier'] is True:
    path  = '/'+shell.config['identity']+'/barrier'
  else:
    path  = '/'+shell.config['identity']
  value = json.dumps({'NodeId':shell.config['nodeid']}, encoding='utf-8')

  try:
    zk.create(path, value=value, acl=None, ephemeral=True, sequence=(not shell.config['barrier']), makepath=True)
  except NodeExistsError as e:
    pass
  except:
    logging.error(e)
    sys.exit(1)
  else:
    logging.info("Node %s created with value %s" %(path, value))


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
      zk.handler.spawn(create_ephemeral)


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
          zk.handler.spawn(create_ephemeral)
      

  zk.add_listener(my_listener)

  zk.start()

def query_barrier(identity):
  path = '/'+identity+'/barrier'
  if zk.exists(path):
    try:
      (value, stat) = zk.get(path)
      logging.info("Master is %s" %value)
      value = json.loads(value)
      return value['NodeId']
    except Exception as e:
      logging.warn("Master querying failed")
      logging.warn(e)
      return None
  else:
    logging.warn("Master querying failed")
    return None


def query_lowest(identity):
  global offset
  path = '/'+identity
  names = []
  values = []
  lowest_v = sys.maxint
  lowest_i = []

  try:
    names = zk.get_children(path)
  except:
    return None
  for name in names:
    try:
      value = zk.get(name)
    except:
      names.remove(name)
    else:
      values.append(value['TaskSum'])

  for i in range(len(values)):
    if values[i] < lowest_v:
      lowest_v = values[i]

  for i in range(len(values)):
    if values[i] == lowest_v:
      lowest_i.append(i)

  offset = offset + 1
  if offset >= len(lowest_i):
    offset = 0

  return names[offset]

def update_payload(identity,payload):
  try:
    names = zk.get_children(path)
  except:
    return False
  for name in names:
    try:
      value = zk.get(name)
    except:
      names.remove(name)
    else:
      if shell.config['NodeId'] == value['NodeId']:
        break
  else:
    return False

  for (k,v) in payload:
    value[k] = v

  try:
    zk.set(name, value)
  except:
    return False

  return True


