#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import sys
import os
import logging
import signal
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from zproxy import shell, local, remote, zclient


def main():
  shell.check_python()

  shell.get_config()

  try:
    logging.info("starting local at %s:%d" %
                 (shell.config['local_address'], shell.config['local_port']))

    def int_handler(signum, _):
      logging.warn('received SIGINIT, doing graceful shutting down..')
      #free resource
      sys.exit(1)
    signal.signal(signal.SIGINT, int_handler)

  except Exception as e:
    shell.print_exception(e)
    sys.exit(1)

#  remote.svrInit()

  zclient.start()

  local.start()

  while True:
    time.sleep(5)


if __name__ == '__main__':
    main()
