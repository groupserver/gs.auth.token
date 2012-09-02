# coding=utf-8
from operator import or_
from zope.component import createObject
from audit import Auditor, AUTH_FAIL
from authtoken import AuthenticationTokenMismatch


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
