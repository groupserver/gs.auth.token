# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals
from mock import MagicMock
from unittest import TestCase
import gs.auth.token.createtoken


class TestCreateToken(TestCase):
    'Test the functions in the createtoken module.'

    def setUp(self):
        gs.auth.token.createtoken.create_engine = MagicMock()
        gs.auth.token.createtoken.MetaData = MagicMock()
        gs.auth.token.createtoken.Table = MagicMock()

    def test_create_token(self):
        'Test the create_token function'
        c = gs.auth.token.createtoken.create_token()
        d = gs.auth.token.createtoken.create_token()
        self.assertNotEqual(c, d)

    def test_delete_old_tokens_from_db(self):
        'Test the delete_old_tokens_from_db function'
        t = MagicMock()
        gs.auth.token.createtoken.delete_old_tokens_from_db(t)
        self.assertEqual(1, t.delete.call_count)

    def test_add_token_to_db(self):
        'Test the add_token_to_db function'
        t = MagicMock()
        fauxToken = 'foo'
        gs.auth.token.createtoken.add_token_to_db(t, fauxToken)
        self.assertEqual(1, t.insert.call_count)
        args, kwargs = t.insert.call_args
        d = args[0]
        self.assertIn('gs.auth.token', d.values())
        self.assertIn(fauxToken, d.values())
