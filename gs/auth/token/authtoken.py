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
from zope.schema import ASCIILine, ValidationError
from gs.option import ComponentOptions


class AuthenticationTokenMismatch(ValidationError):
    """The authentication token does not match the one in the system"""
    def __init__(self, value):
        self.value = value

    def __unicode__(self):
        return 'The authentication token "%s" does not match the one '\
            'in the database.' % self.value

    def __str__(self):
        return unicode(self).encode('ascii', 'ignore')

    def doc(self):
        return self.__str__()


class AuthToken(ASCIILine):
    '''Authentication Token Field

This is used as a simple way to verify who is pushing the a form: the
value of this field is checked agaist the one in the database. If they
are the same then all is good; if they are different an
AuthenticationTokenMismatch is raised.'''
    def constraint(self, value):
        options = ComponentOptions(self.context, 'gs.auth.token')
        authToken = options.get('authToken')
        if value != authToken:
            raise AuthenticationTokenMismatch(value)
        return True
