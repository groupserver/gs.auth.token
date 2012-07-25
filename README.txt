Introduction
============

Token-authentication is used to allow server-side scripts to access forms
in `GroupServer`_. It is the simplest authentication method provided by the
system:

* You `create a token`_
* You `add authentication to a form`_
* A submitted a server-side scripts looks up token from the database.
* The token is passed in as part of the ``POST`` request that is made to
  submit the form.
* GroupServer checks the token with the one in the database, and throws a
  validation-error if they do not match.

The scripts that use this product usually require `authentication
configuration`_.

Create a Token
==============

The console-script ``gs_auth_token_create`` creates a new token and adds it
to the relational database. Once run it is necessary to change the
`authentication configuration`_.

Synopsis
--------
::

   gs_auth_token_create [-h] dsn

Arguments
---------

``dsn``:
  The data source name (DSN) in the form
  ``postgres://user:password@host:port/database_name``. The configuration
  file for GroupServer (normally ``etc/gsconfig.ini``) lists all the DSN
  entries for the system.


Optional Arguments
~~~~~~~~~~~~~~~~~~

``-h``, ``--help``
  Print the help message and exit.


Examples
~~~~~~~~

Generate a new token and place it in the ``production`` database. In this
example PostgreSQL is running on the local machine, and has as been set up
so authentication is unnecessary::

   gs_auth_token_create posgres://localhost/production

Generate a new token and place it in the ``testing`` database on a remote
machine. Authentication is used::

   gs_auth_token_create posgres://remoteUser:password@remote.machine.name/testing

Add Authentication to a Form
============================

To add authentication to a form first you add the ``AuthToken`` `field`_ to
the form interface. Then, in the error handler, you add `logging`_.

Field
-----

For ``zope.formlib`` forms [#formlib]_ adding authentication requires the
use of the ``AuthToken`` field::

  from zope.interface.interface import Interface
  from gs.auth.token import AuthToken

  class ISomeForm(Interface):

      token = AuthToken(title=u'Token',
                        description=u'The authentication token',
                        required=True)

The ``AuthToken`` field checks its input against the stored token, and
throws a ``AuthenticationTokenMismatch`` error if there is a mismatch (in
which case the `logging`_ takes over)

Logging
-------

If there is an error in the form then the utility ``log_auth_error`` should
be called::
  
  log_auth_error(context, request, errors)

This utility will check for the ``AuthenticationTokenMismatch`` error in the
list of ``errors``. If present it will add an audit-event to the audit-trail
table.

Authentication Configuration
============================

The script that requires authentication may be running on a machine that is
separate to the GroupServer system, which may use a database that is on a
third machine! Because of this the **scripts** rarely read the
authentication token from the relational database. Instead they typically
use a configuration file for storing the token. See the documentation for
``smtp2gs`` for more examples [#smtp2gs]_.

The script to `create a token`_ does not change these configuration
files. Instead it displays the new token and the administrator must change
the entries in the configuration.

.. [#formlib] GroupServer uses ``zope.formlib`` for most of its forms: 
   <http://docs.zope.org/zope.formlib/>.
.. [#smtp2gs] See ``gs.group.messages.add.smtp2gs`` 
            <https://source.iopen.net/groupserver/gs.group.messages.add.smtp2gs/summary>
.. _GroupServer: http://groupserver.org/
