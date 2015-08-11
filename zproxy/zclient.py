#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import logging
import json
import sys
import os

from kazoo.client import KazooClient
from kazoo.protocol.states import *
from kazoo.exceptions import *

from zproxy import shell

zk = None
offset = -1


def create_ephemeral():
  if not shell.config['barrier']:
    path  = '/'+shell.config['identity']+'/'
    value = json.dumps({'NodeId':shell.config['nodeid'],'TaskSum':0}, encoding='utf-8')
    sequence = True
  else:
    path  = '/'+shell.config['identity']+'/barrier'
    value = json.dumps({'NodeId':shell.config['nodeid']}, encoding='utf-8')
    sequence = False

  try:
    ret = zk.create(path, value=value, acl=None, ephemeral=True, sequence=sequence, makepath=True)
  except NodeExistsError as e:
    pass
  except Exception as e:
    logging.error(e)
    sys.exit(1)
  else:
    logging.info("Node %s created with value %s" %(ret, value))


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

  try:
    zk.start()
  except Exception as e:
    logging.error(e)
    sys.exit(1)


def query_owned_node(path):
  nodeid = None
  desc = None

  if not path:
    path = "Identity is empty"
  else:
    if zk.exists(path):
      try:
        (value, junk) = zk.get(path)
        value = json.loads(value)
      except Exception as e:
        desc = "Operating zookeeper failed %s" %e
      else:
        nodeid = value['NodeId']
    else:
      desc = "%s dosent exist" %path
  return (nodeid,desc)


def remove_owned_node(path):
  desc = None

  if not path:
    desc = "path is empty"
  else:
    if zk.exists(path):
      try:
        (value, junk) = zk.get(path)
        value = json.loads(value)
      except Exception as e:
        desc = "Operating zookeeper failed %s" %e
      else:
        if shell.config['nodeid'] ==  value['NodeId']:
          zk.delete(path)
        else:
          desc = "NodeId:%d is not Master" %shell.config['nodeid']
    else:
      desc = "Master doesnt exist under %s" %identity
  return desc


def update_owned_childnode(path,payload):
  desc = None

  try:
    nodes = zk.get_children(path)
  except Exception as e:
    desc = "Operating zookeeper failed: %s" %e
  else:
    for node in nodes:
      try:
        (value,junk) = zk.get("%s/%s" %(path, node))
        value = json.loads(value, encoding='UTF-8')
      except Exception as e:
        nodes.remove(node)
      else:
        if shell.config['nodeid'] == value['NodeId']:
          break
    else:
      desc = "Cannot find NodeId:%s from children of %s" %(shell.config['nodeid'], path)

    if not desc:
      for (k,v) in payload.items():
          value[k] = v

      try:
        value = json.dumps(value)
        zk.set("%s/%s" %(path, node), value)
      except:
        desc = "Operating zookeeper failed %s" %e

  return desc


def query_lowest_childnode(path):
  global offset
  nodes = []
  values = []
  nodeids = []
  lowest_v = sys.maxint
  lowest_i = []
  nodeid = None
  desc = None

  try:
    nodes = zk.get_children(path)
  except Exception as e:
    desc = "Operating zookeeper failed %s" %e
  else:
    for node in nodes:
      try:
        (value,junk) = zk.get("%s/%s" %(path, node))
        value = json.loads(value, encoding='UTF-8')
      except:
        nodes.remove(node)
      else:
        values.append(value['TaskSum'])
        nodeids.append(value['NodeId'])

    if not nodeids:
      desc = "Operating(get) zookeeper failed"
    else:
      for i in range(len(values)):
        if int(values[i]) < lowest_v:
          lowest_v = int(values[i])

      for i in range(len(values)):
        if values[i] == lowest_v:
          lowest_i.append(i)

      offset = offset + 1
      if offset >= len(lowest_i):
        offset = 0

      nodeid = nodeids[offset]

  return (nodeid,desc)


def export_tree(path):
  tree = {}
  children = []

  tree['name'] = path
  try:
    value,junk = zk.get(path)
  except Exception as e:
    tree['value'] = "%s" %e
    logging.warn(e)
  else:
    try:
      value_d = json.loads(value)
    except Exception as e:
      tree['value'] = value
    else:
      tree['value'] = value_d

  try:
    nodes = zk.get_children(path)
  except Exception as e:
    logging.warn(e)
  else:
    if nodes:
      for node in nodes:
        path_c = os.path.join(path,node)
        if path_c == "/zookeeper":
          continue
        children.append(export_tree(path_c))
        tree['children'] = children

  return tree

