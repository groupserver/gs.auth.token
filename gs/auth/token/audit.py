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
from datetime import datetime
SUBSYSTEM = 'gs.auth.token'
from logging import getLogger
log = getLogger(SUBSYSTEM)
from zope.component.interfaces import IFactory
from pytz import UTC
from zope.interface import implements, implementedBy
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, \
    AuditQuery
from Products.XWFCore.XWFUtils import munge_date
from .createtoken import create_token  # A tiny HACK, but it works.

UNKNOWN = '0'
AUTH_FAIL = '1'


class AuditEventFactory(object):
    implements(IFactory)

    def __call__(self, context, event_id, code, date,
        userInfo, instanceUserInfo, siteInfo, groupInfo=None,
        instanceDatum='', supplementaryDatum='', subsystem=''):
        if code == AUTH_FAIL:
            event = AuthFailEvent(context, event_id, date, siteInfo,
                                  instanceDatum)
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date,
                      userInfo, instanceUserInfo, siteInfo, groupInfo,
                      instanceDatum, supplementaryDatum, SUBSYSTEM)
        assert event
        return event

    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)


# AUTH_FAIL       = '1'
class AuthFailEvent(BasicAuditEvent):
    ''' An audit-trail event representing an authentication failure.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, siteInfo, pageId):
        BasicAuditEvent.__init__(self, context, id, AUTH_FAIL, d, None, None,
                                 siteInfo, None, pageId, None, SUBSYSTEM)

    def __str__(self):
        retval = 'Authentication failure for the page <%s> on the site %s '\
            '(%s).' % (self.instanceDatum, self.siteInfo.name,
                        self.siteInfo.id)
        retval = retval.encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event gs-group-messages-add-%s' % self.code
        retval = '<span class="%s">Failed authentication '\
            'for the page <cite>%s</cite> on %s.' % \
            (cssClass, self.instaceDatum, self.siteInfo.name)
        retval = '%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval


class Auditor(object):
    def __init__(self, context, siteInfo):
        self.context = context
        self.siteInfo = siteInfo

        self.queries = AuditQuery()
        self.factory = AuditEventFactory()

    def info(self, code, instanceDatum=''):
        d = datetime.now(UTC)
        eventId = create_token()

        e = self.factory(self.context, eventId, code, d,
                         None, None, self.siteInfo, None,
                         instanceDatum, None, SUBSYSTEM)

        self.queries.store(e)
        log.info(e)
