# coding=utf-8
from zope.schema import ASCIILine, ValidationError
from gs.option import ComponentOptions

class AuthenticationTokenMismatch(ValidationError):
    """The authentication token does not match the one in the system"""
    def __init__(self, value):
        self.value = value
        
    def __unicode__(self):
        return u'The authentication token "%s" does not match the one '\
            u'in the database.' % self.value
            
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
