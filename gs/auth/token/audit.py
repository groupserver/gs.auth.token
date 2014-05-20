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
SUBSYSTEM = 'gs.auth.token'
from logging import getLogger
log = getLogger(SUBSYSTEM)
from zope.interface import implementedBy
from Products.GSAuditTrail import BasicAuditEvent, AuditQuery
from gs.core import curr_time, to_id

UNKNOWN = '0'
AUTH_FAIL = '1'


class AuditEventFactory(object):

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

    def __init__(self, context, id, d, siteInfo, pageId):
        BasicAuditEvent.__init__(self, context, id, AUTH_FAIL, d, None, None,
                                 siteInfo, None, pageId, None, SUBSYSTEM)

    def __unicode__(self):
        retval = 'Authentication failure for the page <%s> on the site %s '\
            '(%s).' % (self.instanceDatum, self.siteInfo.name,
                        self.siteInfo.id)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event gs-group-messages-add-{0}'.format(self.code)
        r = '<span class="{0}">Failed authentication for the page '\
            '<cite>{1}</cite> on {2}.'
        retval = r.format(cssClass, self.instaceDatum, self.siteInfo.name)
        retval = '%s (%s)' % \
          (retval, self.date.strftime('%F %T %Z'))
        return retval


class Auditor(object):
    def __init__(self, context, siteInfo):
        self.context = context
        self.siteInfo = siteInfo

        self.queries = AuditQuery()
        self.factory = AuditEventFactory()

    def info(self, code, instanceDatum=''):
        d = curr_time()
        eventId = to_id(code, instanceDatum)

        e = self.factory(self.context, eventId, code, d,
                         None, None, self.siteInfo, None,
                         instanceDatum, None, SUBSYSTEM)

        self.queries.store(e)
        log.info(e)
