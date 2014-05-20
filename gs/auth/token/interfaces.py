# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2012, 2014 OnlineGroups.net and Contributors.
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
from zope.interface.interface import Interface
from zope.schema import TextLine
from gs.option.converter import GSOptionConverterFactory


class IGSAuthTokenOptions(Interface):
    authToken = TextLine(title='Authentication Token',
                         description='A token to allow the non-Zope parts of '
                             'the system to access Zope pages, without needing '
                             'passwords and other gumf.')
        # See the authtoken module for more info


class GSAuthTokenOptionFactory(GSOptionConverterFactory):
    interface = IGSAuthTokenOptions
