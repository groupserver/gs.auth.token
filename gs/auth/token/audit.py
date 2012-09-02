# coding=utf-8
from pytz import UTC
from datetime import datetime
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, \
    AuditQuery
from Products.XWFCore.XWFUtils import munge_date
from createtoken import create_token  # A tiny HACK, but it works.

SUBSYSTEM = 'gs.auth.token'
import logging
log = logging.getLogger(SUBSYSTEM)  #@UndefinedVariable

UNKNOWN   = '0'
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
        retval = u'Authentication failure for the page <%s> on the site %s '\
            u'(%s).' % (self.instanceDatum, self.siteInfo.name,
                        self.siteInfo.id)
        retval = retval.encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = u'audit-event gs-group-messages-add-%s' % self.code
        retval = u'<span class="%s">Failed authentication '\
            u'for the page <cite>%s</cite> on %s.' % \
            (cssClass, self.instaceDatum, self.siteInfo.name)
        retval = u'%s (%s)' % \
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
