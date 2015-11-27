# -*- coding: utf-8 -*-
# Copyright (c) Rackspace US, Inc.
# See LICENSE for details.
"""
Tests for L{udplog.cli}.
"""

from __future__ import division, absolute_import

from twisted.python import usage
from twisted.trial.unittest import TestCase

from udplog.cli import SendOptions

class SendOptionsTests(TestCase):
    """
    Tests for L{udplog.cli.SendOptions}.
    """

    def test_message(self):
        """
        Non-option arguments are the log message.
        """
        options = ["foo"]
        config = SendOptions()
        config.parseOptions(options)
        self.assertEqual('foo', config['message'])


    def test_messageMultiple(self):
        """
        Multiple non-option arguments are joined by spaces.
        """
        options = ["foo", "bar"]
        config = SendOptions()
        config.parseOptions(options)
        self.assertEqual('foo bar', config['message'])


    def test_messageEmpty(self):
        """
        An empty log message raises an exception.
        """
        options = [""]
        config = SendOptions()
        exc = self.assertRaises(usage.UsageError, config.parseOptions,
                                                  options)
        self.assertEqual("No log message provided", str(exc))


    def test_messageMissing(self):
        """
        Not providing a message raises an exception.
        """
        options = []
        config = SendOptions()
        exc = self.assertRaises(usage.UsageError, config.parseOptions,
                                                  options)
        self.assertEqual("No log message provided", str(exc))


    def test_category(self):
        """
        The log category is parsed.
        """
        options = ["--category=foo", "bar"]
        config = SendOptions()
        config.parseOptions(options)
        self.assertEqual("foo", config['category'])


    def test_categoryEmpty(self):
        """
        An empty log category raises an exception.
        """
        options = ["--category="]
        config = SendOptions()
        exc = self.assertRaises(usage.UsageError, config.parseOptions,
                                                  options)
        self.assertEqual("No log category provided", str(exc))


    def test_extra(self):
        """
        Extra fields as JSON are merged in.
        """
        options = ["""--extra={"foo": "baz"}""", "bar"]
        config = SendOptions()
        config.parseOptions(options)
        self.assertEqual("baz", config['extra']['foo'])


    def test_extraMessage(self):
        """
        The log message may also be provided in the extra fields.
        """
        options = ["""--extra={"message": "bar"}"""]
        config = SendOptions()
        config.parseOptions(options)
        self.assertEqual("bar", config['message'])
