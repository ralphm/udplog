# -*- test-case-name: udplog.test.test_cli -*-
# Copyright (c) Rackspace US, Inc.
# See LICENSE for details.

"""
Command line script entry points.
"""

from __future__ import division, absolute_import

import socket
import sys
from os import path

import simplejson

from twisted.python import usage

from udplog import udplog

LEVEL_NAMES = {'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'}

class SendOptions(usage.Options):
    synopsis = ("udplog-send --category=category [options] message ...\n"
                "udplog-send --extra=json [options]")
    optParameters = [
        ['category', 'c', 'udplog_unknown',
         "The type of log event"],
        ['level', 'l', 'INFO',
         "The log level"],
        ['appname', 'a', 'udplog-send',
         "The name of the application emitting the log event"],
        ['extra', 'e', None,
         "A JSON object (dictionary) of event fields to be merged into the "
             "emitted event"],
        ['udplog-host', 'h', udplog.DEFAULT_HOST,
         "The hostname of the UDPLog server"],
        ['udplog-port', 'p', udplog.DEFAULT_PORT,
         "The portname of the UDPLog server"],
    ]

    def parseArgs(self, *args):
        self['message'] = (" ".join(args)).decode('utf-8')


    def postOptions(self):
        if self['extra']:
            try:
                self['extra'] = simplejson.loads(self['extra'])
            except Exception, exc:
                raise usage.UsageError("Could not parse extra fields as a "
                                       "JSON object: %s" % (exc,))
        else:
            self['extra'] = {}

        if self['extra'].get('category'):
            self['category'] = self['extra']['category']

        if self['extra'].get('message'):
            self['message'] = self['extra']['message']

        if self['extra'].get('logLevel'):
            self['level'] = self['extra']['logLevel']

        if not self['category']:
            raise usage.UsageError("No log category provided")

        if not self['message']:
            raise usage.UsageError("No log message provided")

        self['level'] = self['level'].upper()
        if self['level'] not in LEVEL_NAMES:
            raise usage.UsageError("Log level must be one of " +
                                   ", ".join(LEVEL_NAMES))

def send(options=None):
    config = SendOptions()
    try:
        config.parseOptions(options)
    except usage.UsageError, exc:
        name = path.basename(sys.argv[0])
        print "%s: %s" % (name, exc)
        print "%s: Try --help for usage details." % (name,)
        return 1

    eventDict = {
        'message': config['message'],
        'logLevel': config['level'],
        'appname': config['appname'],
    }

    eventDict.update(config['extra'])

    eventDict.setdefault('hostname', socket.gethostname())

    logger = udplog.UDPLogger()
    logger.log(config['category'], eventDict)

    return 0
