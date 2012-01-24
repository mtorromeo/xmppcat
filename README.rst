xmppcat
=======

A unix command line program that works like *cat* but sends its output through XMPP.

Help
----

::

	usage: xmppcat [-h] [-V] [-c CONFIG] [-H HOST] [-P PORT] [-u USER] [-p PWD]
	               [-q] [-d] [-v]
	               recipient [file]

	CLI application that works like cat but sends its output through xmpp

	positional arguments:
	recipient             The XMPP jid to send the message to
	file                  The file to read. If not specified it will be read
	                      from STDIN

	optional arguments:
	-h, --help            show this help message and exit
	-V, --version         show program's version number and exit
	-c CONFIG, --config CONFIG
	                      Use a different configuration file
	-H HOST, --host HOST  XMPP host (xmppcat will try to auto detect it with DNS
	                      or JID parsing)
	-P PORT, --port PORT  XMPP port
	-u USER, --user USER  XMPP username (JID)
	-p PWD, --pass PWD    XMPP password

	output arguments:
	-q, --quiet           Suppress any non-error output
	-d, --debug           Enable debugging output
	-v, --verbose         Show additional connection informations

Configuration file
------------------

The program requires several arguments to be specified in order to be able to connect and authenticate to a XMPP server.
To simplify this process you can save this options in a configuration file, either globally in */etc/xmppcat.conf* or locally in *$HOME/.xmppcat.conf*.

This is an example of a configuration file for xmppcat::

	[DEFAULT]
	user = myuser@jabber.org/xmppcat
	pass = mypassword
	host = jabber.org # can be autodetected by dnspython
	port = 5222 # also autodetectable

Example usage
-------------

::

	echo "Hello world!" | xmppcat recipient@jabber.org
	xmppcat recipient@jabber.org file.txt

LICENSE
-------
Copyright (c) 2012 Massimiliano Torromeo

xmppcat is free software released under the terms of the BSD license.

See the LICENSE file provided with the source distribution for full details.

Contacts
--------

* Massimiliano Torromeo <massimiliano.torromeo@gmail.com>