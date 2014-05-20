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
from argparse import ArgumentParser
from random import SystemRandom
from string import printable
import sys
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import OperationalError, ArgumentError
from sqlalchemy.sql import and_
from gs.core import convert_int2b62

EXIT_VALS = {
    'success': 0,
    'db_create_engine': 10,
    'db_connect': 11,
}


B62_ALPHABET = printable[:62]


def create_token():
    randomNumberGenerator = SystemRandom()
    randomInteger = randomNumberGenerator.randint(0, 62 ** 32)
    token = convert_int2b62(randomInteger)
    return token


def delete_old_tokens_from_db(table):
    d = table.delete(and_(table.c.component_id == 'gs.auth.token',
                          table.c.option_id == 'authToken'))
    d.execute()


def add_token_to_db(table, token):
    data = {
        'component_id': 'gs.auth.token',
        'option_id': 'authToken',
        'site_id': '',
        'group_id': '',
        'value': token, }
    i = table.insert(data)
    i.execute()


def main():
    d = 'Generate a new authentication token, and add it to the database.'
    e = 'Running this script will invalidate all the existing tokens used to '\
        'authenticate the scripts, such as "smtp2gs". The configuration for '\
        'these scripts will have to be manually updated.'
    p = ArgumentParser(description=d, epilog=e)
    p.add_argument('dsn', metavar='dsn',
                   help='The data source name (DSN) in the form '
                       '"postgres://user:password@host:port/database_name".')
    args = p.parse_args()
    try:
        engine = create_engine(args.dsn, echo=False)
    except ArgumentError as ae:
        m = '%s: Could not create the token because of an error connecting\n'\
            'to the database:\n%s\n\nPlease check the DSN and try again.' %\
            (p.prog, ae.message)
        m = m.replace('\n', '\n%s: ' % p.prog) + '\n'
        sys.stderr.write(m)
        sys.exit(EXIT_VALS['db_create_engine'])

    try:
        connection = engine.connect()  # lint:ok
    except OperationalError as oe:
        m = '%s: Could not create the token because of an error connecting\n'\
            'to the database:\n%s\n Please check the DSN and try again.' % \
            (p.prog, oe.orig.message.replace('FATAL: ', ''),)
        m = m.replace('\n', '\n%s: ' % p.prog) + '\n'
        sys.stderr.write(m)
        sys.exit(EXIT_VALS['db_connect'])
    metadata = MetaData()
    metadata.bind = engine
    table = Table('option', metadata, autoload=True)

    delete_old_tokens_from_db(table)

    token = create_token()
    add_token_to_db(table, token)

    m = 'The authentication token has been changed to the following:\n    '\
        '%s\n\nPlease update the relevant configuration files.\n' % (token,)
    sys.stdout.write(m)
    sys.exit(EXIT_VALS['success'])

if __name__ == '__main__':
    main()
