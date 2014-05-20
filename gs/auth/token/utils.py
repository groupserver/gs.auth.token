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
from operator import or_
from zope.component import createObject
from .audit import Auditor, AUTH_FAIL
from .authtoken import AuthenticationTokenMismatch


def log_auth_error(context, request, errors):
    assert context
    assert request
    authError = reduce(or_, [isinstance(e[2], AuthenticationTokenMismatch)
                             for e in errors],
                       False)
    if authError:
        siteInfo = createObject('groupserver.SiteInfo', context)
        auditor = Auditor(context, siteInfo)
        auditor.info(AUTH_FAIL, request.URL)
