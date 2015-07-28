#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import sys
import os
import logging
import signal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from zproxy import shell


def main():
    shell.check_python()

    config = shell.get_config()

    try:
        logging.info("starting local at %s:%d" %
                     (config['local_address'], config['local_port']))

        def int_handler(signum, _):
            logging.warn('received SIGINIT, doing graceful shutting down..')
            #free resource
            sys.exit(1)
        signal.signal(signal.SIGINT, int_handler)

        #loop.run()
    except Exception as e:
        shell.print_exception(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
