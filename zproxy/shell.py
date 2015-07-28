#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import os
import json
import sys
import getopt
import logging
from zproxy.common import to_bytes, to_str


VERBOSE_LEVEL = 5

verbose = 0


def check_python():
  info = sys.version_info
  if info[0] == 2 and not info[1] >= 6:
    print('Python 2.6+ required')
    sys.exit(1)
  elif info[0] == 3 and not info[1] >= 3:
    print('Python 3.3+ required')
    sys.exit(1)
  elif info[0] not in [2, 3]:
    print('Python version not supported')
    sys.exit(1)


def print_exception(e):
  global verbose
  logging.error(e)
  if verbose > 0:
    import traceback
    traceback.print_exc()


def print_version():
  version = ''
  try:
    import pkg_resources
    version = pkg_resources.get_distribution('zproxy').version
  except Exception as e:
    #pass
    print_exception(e)
  print('zproxy %s' % version)


def find_config():
  config_path = 'config.json'
  if os.path.exists(config_path):
    return config_path
  config_path = os.path.join(os.path.dirname(__file__), 'config.json')
  if os.path.exists(config_path):
    return config_path
  return None


def check_config(config):
  if 'local_port' in config:
    config['local_port'] = int(config['local_port'])

  if 'server_port' in config and type(config['server_port']) != list:
    config['server_port'] = int(config['server_port'])

  if config.get('local_address', '') in [b'0.0.0.0']:
    logging.warn('warning: local set to listen on 0.0.0.0, it\'s not safe')

  if config.get('server', '') in ['127.0.0.1', 'localhost']:
    logging.warn('warning: server set to listen on %s:%s, are you sure?' %
           (to_str(config['server']), config['server_port']))

  if config.get('identity', None) is None:
    logging.error('identity can\'t default to none')
    sys.exit(1)


def get_config():
  global verbose

  logging.basicConfig(level=logging.INFO,
                      format='%(levelname)-s: %(message)s')

  shortopts = 'hc:vqs:p:l:a:b:d:k:i:'
  longopts = ['help', 'version', 'log-file']

  try:
    config_path = find_config()
    optlist, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
    for key, value in optlist:
      if key == '-c':
        config_path = value

    if config_path:
      logging.info('loading config from %s' % config_path)
      with open(config_path, 'rb') as f:
        try:
          config = json.loads(f.read().decode('utf8'),
                              object_hook=_decode_dict)
        except ValueError as e:
          logging.error('found an error in config.json: %s',
                         e.message)
          sys.exit(1)
    else:
      config = {}

    v_count = 0
    for key, value in optlist:
      if key == '-s':
        config['server'] = to_str(value)
      elif key == '-p':
          config['server_port'] = int(value)
      elif key == '-l':
        config['local_port'] = int(value)
      elif key == '-a':
        config['local_address'] = to_str(value)
      elif key == '-b':
        config['barrier'] = True
      elif key == '-d':
        config['identity'] = to_str(value)
      elif key == '-v':
        v_count += 1
        # '-vv' turns on more verbose mode
        config['verbose'] = v_count
      elif key in ('-h', '--help'):
        print_help()
        sys.exit(0)
      elif key == '--version':
        print_version()
        sys.exit(0)
      elif key == '--log-file':
        config['log-file'] = to_str(value)
      elif key == '-k':
        config['des3-key'] = to_str(value)
      elif key == '-i':
        config['des3-iv'] = to_str(value)
      elif key == '-q':
        v_count -= 1
        config['verbose'] = v_count
  except getopt.GetoptError as e:
    print(e, file=sys.stderr)
    print_help()
    sys.exit(2)

  if not config:
    logging.error('config not specified')
    print_help()
    sys.exit(2)

  config['log-file'] = config.get('log-file', '/var/log/zproxy.log')
  config['verbose'] = config.get('verbose', False)
  config['local_address'] = to_str(config.get('local_address', '0.0.0.0'))
  config['local_port'] = config.get('local_port', 1080)
  config['server'] = to_str(config.get('server', '127.0.0.1'))
  config['server_port'] = config.get('server_port', 2181)
  config['des3-key'] = to_str(config.get('des3-key', 'D^=^vGfAdUTixobQP$HhsTsa'))
  config['des3-iv'] = to_str(config.get('des3-iv', 'aVtsvC#S'))
  config['barrier'] = config.get('barrier', False)

  logging.getLogger('').handlers = []
  logging.addLevelName(VERBOSE_LEVEL, 'VERBOSE')
  if config['verbose'] >= 2:
    level = VERBOSE_LEVEL
  elif config['verbose'] == 1:
    level = logging.DEBUG
  elif config['verbose'] == -1:
    level = logging.WARN
  elif config['verbose'] <= -2:
    level = logging.ERROR
  else:
    level = logging.INFO
  verbose = config['verbose']
  logging.basicConfig(level=level,
            format='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

  check_config(config)

  sys.stdin.close()
  try:
    freopen(config['log_file'], 'a', sys.stdout)
    freopen(config['log_file'], 'a', sys.stderr)
  except IOError as e:
    shell.print_exception(e)
    sys.exit(1)

  return config


def print_help():
    print('''usage: zproxy [OPTION]...
A client of Zookeeper

You can supply configurations via either config file or command line arguments.

Proxy options:
  -c CONFIG              path to config file
  -s SERVER_ADDR         server address
  -p SERVER_PORT         server port, default: 8388
  -a LOCAL_ADDR          local binding address, default: 127.0.0.1
  -l LOCAL_PORT          local port, default: 1080
  -d IDENTITY            identity
  -b BARRIER             barrier mode
  -k DES3_KEY            key for des3 encryption
  -i DES3_IV             iv  for des3 encryption

General options:
  -h, --help             show this help message and exit
  --log-file LOG_FILE    log file
  -v, -vv                verbose mode
  -q, -qq                quiet mode, only show warnings/errors
  --version              show version information

''')
