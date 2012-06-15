# coding=utf-8
from zope.interface.interface import Interface
from zope.schema import TextLine
from gs.option.converter import GSOptionConverterFactory

class IGSAuthTokenOptions(Interface):
    authToken = TextLine(title=u'Authentication Token',
                         description=u'A token to allow the non-Zope parts of '
                         u'the system to access Zope pages, without needing '
                         u'passwords and other gumf.')
        # See the authtoken module for more info

class GSAuthTokenOptionFactory(GSOptionConverterFactory):
    interface = IGSAuthTokenOptions
