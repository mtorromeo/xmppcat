#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Massimiliano Torromeo <massimiliano.torromeo@gmail.com>
# License: BSD

name = "xmppcat"
description = "CLI application that works like cat but sends its output through xmpp"
version = "0.1"
url = "http://github.com/mtorromeo/xmppcat"

import os, sys

def main():
    import setproctitle
    import argparse
    import configparser
    import logging
    from .bot import SendMsgBot

    setproctitle.setproctitle(name)

    parser = argparse.ArgumentParser(prog=name, description=description)

    parser.add_argument('-V', '--version', action='version', version="%(prog)s "+version)
    parser.add_argument('-c', '--config', help='Use a different configuration file')
    parser.add_argument('-H', '--host', help='XMPP host (%(prog)s will try to auto detect it with DNS or JID parsing)')
    parser.add_argument('-P', '--port', help='XMPP port', type=int, default=5222)
    parser.add_argument('-u', '--user', help='XMPP username (JID)')
    parser.add_argument('-p', '--pass', dest='pwd', help='XMPP password')
    parser.add_argument('recipient', nargs=1, help='The XMPP jid to send the message to')
    parser.add_argument('file', nargs='?', help='The file to read. If not specified it will be read from STDIN')

    # Output verbosity options.
    default_loglevel = logging.WARNING
    group = parser.add_argument_group('output arguments')
    group.add_argument('-q', '--quiet', help='Suppress any non-error output', action='store_const', dest='loglevel', const=logging.ERROR, default=default_loglevel)
    group.add_argument('-d', '--debug', help='Enable debugging output', action='store_const', dest='loglevel', const=logging.DEBUG, default=default_loglevel)
    group.add_argument('-v', '--verbose', help='Show additional connection informations', action='store_const', dest='loglevel', const=logging.INFO, default=default_loglevel)

    args = parser.parse_args()

    config = configparser.SafeConfigParser( defaults = dict(status_url = "http://127.0.0.1/server-status") )
    try:
        if args.config:
            config.read( args.config )
        else:
            config.read( ["/etc/{}.conf".format(name), os.path.expanduser("~/.{}.conf".format(name))] )
    except configparser.Error as e:
        sys.exit(e.message)

    config = config['DEFAULT']

    recipient = args.recipient[0]
    if args.file:
        with open(args.file, 'r') as f:
            message = f.read()
    else:
        message = sys.stdin.read()
    pwd = args.pwd if args.pwd else config.get('pass', '')
    user = args.user if args.user else config.get('user', '')

    # Logging
    logging.basicConfig(level=args.loglevel, format='%(levelname)-8s %(message)s')

    server_options = list()
    if args.host:
        server_options.append( (args.host, args.port) )

    xmpp = SendMsgBot(user, pwd, recipient, message)
    if xmpp.connect( *server_options ):
        xmpp.process(block=True)
    else:
        sys.exit("Unable to connect.")

if __name__ == '__main__':
    main()
