# coding=utf-8
from argparse import ArgumentParser
from md5 import new as new_md5
from random import SystemRandom
from string import printable
from sys import argv, stdout

from sqlalchemy import create_engine, BoundMetaData, Table
from sqlalchemy.sql import and_

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

if __name__ == '__main__':
    p = ArgumentParser(description='Generate and add a token to the database.')
    p.add_argument('dbName', metavar='databaseName',
                   help='The name of the database to connect to.')
    p.add_argument('dbUser', metavar='databaseUser',
                   help='The user to connect to the database as.')
    p.add_argument('-o', '--host', metavar='host', default='localhost',
                   help='The host to connect to (default "localhost").')
    p.add_argument('-v', '--verbose', action='store_true',
                   help='Turn on verbose output.')
    args = p.parse_args()
    
    dbconn = 'postgres://%s@%s/%s' % (args.dbUser, args.host, args.dbName)
    args.verbose and stdout.write('Connecting to <%s>,\n' % dbconn)
    engine = create_engine(dbconn, echo=False)
    args.verbose and stdout.write('Binding to the metadata,\n')
    metadata = BoundMetaData(engine)
    args.verbose and stdout.write('Creating the table,\n')
    table = Table('option', metadata, autoload=True)

    args.verbose and stdout.write('Deleting the old tokens,\n')
    delete_old_tokens_from_db(table)

    args.verbose and stdout.write('Creating the new token,\n')
    token = create_token()
    args.verbose and stdout.write('Adding the new token to the database,\n')
    add_token_to_db(table, token)
    args.verbose and stdout.write('Finished.\n')
