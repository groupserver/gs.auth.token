# coding=utf-8
from argparse import ArgumentParser
from md5 import new as new_md5
from random import SystemRandom
from string import printable
import sys
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import OperationalError, ArgumentError
from sqlalchemy.sql import and_

exit_vals = {
    'success':             0,
    'db_create_engine':   10,
    'db_connect':         11,
}

B62_ALPHABET = printable[:62]
def convert_int2b62(num, converted=[]):
    mod = num % 62
    rem = num / 62
    converted.append(B62_ALPHABET[mod])
    if rem:
        return convert_int2b62(rem, converted)
    converted.reverse()
    retval = ''.join(converted)
    return retval

def create_token():
    randomNumberGenerator = SystemRandom()
    randomInteger = randomNumberGenerator.randint(0, 62**32)
    token = convert_int2b62(randomInteger)
    return token

def delete_old_tokens_from_db(table):
    d = table.delete(and_(table.c.component_id == 'gs.auth.token', 
                          table.c.option_id == 'authToken'))
    d.execute()

def add_token_to_db(table, token):
    data = {
        'component_id': 'gs.auth.token',
        'option_id':    'authToken',
        'site_id':      '',
        'group_id':     '',
        'value':        token,}
    i = table.insert(data)
    i.execute()

def main():
    d = 'Generate a new authentication token, and add it to the database.'
    e = 'Running this script will invalidate all the existing tokens used to '\
        'authenticate the scripts, such as "smtp2gs". The configuration for '\
        'these scripts will have to be manually updated.'
    p = ArgumentParser(description=d, epilog=e)
    p.add_argument('dsn', metavar='dsn', 
                   help='The data source name (DSN) in the form '\
                       '"postgres://user:password@host:port/database_name".')
    args = p.parse_args()
    try:
        engine = create_engine(args.dsn, echo=False)
    except ArgumentError, ae:
        m = u'%s: Could not create the token because of an error connecting\n'\
            u'to the database:\n%s\n\nPlease check the DSN and try again.' %\
            (p.prog, ae.message)
        m = m.replace(u'\n', u'\n%s: ' % p.prog) + '\n'
        sys.stderr.write(m)
        sys.exit(exit_vals['db_create_engine'])
        
    try:
        connection = engine.connect()
    except OperationalError, oe:
        m = u'%s: Could not create the token because of an error connecting\n'\
            u'to the database:\n%s\n Please check the DSN and try again.' % \
            (p.prog, oe.orig.message.replace('FATAL: ', ''),)
        m = m.replace('\n', '\n%s: ' % p.prog) + '\n'
        sys.stderr.write(m.encode('utf-8', 'ignore'))
        sys.exit(exit_vals['db_connect'])
    metadata = MetaData()
    metadata.bind=engine
    table = Table('option', metadata, autoload=True)

    delete_old_tokens_from_db(table)

    token = create_token()
    add_token_to_db(table, token)

    m = u'The authentication token has been changed to the following:\n    '\
        u'%s\n\nPlease update the relevant configuration files.\n' % (token,)
    sys.stdout.write(m.encode('utf-8', 'ignore'))
    sys.exit(exit_vals['success'])

if __name__ == '__main__':
    main()
