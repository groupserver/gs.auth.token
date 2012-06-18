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

Create a Token
==============

The console-script ``gs_auth_token_create`` creates a new token and adds it
to the relational database. It can be run at any time to crate a new token.

Synopsis
--------
::

   gs_auth_token_create [-h] [-o host] [-v] databaseName databaseUser

Arguments
---------

``databaseName``
  The name of the database to connect to.

``databaseUser``
  The user to connect to the database as.


Optional Arguments
~~~~~~~~~~~~~~~~~~

``-h``, ``--help``
  Print the help message and exit.

``-o``, ``--host``
  The host to connect to (defaults to ``localhost``).

``-v``, ``--verbose``
  Turn on verbose output.

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

.. [#formlib] GroupServer uses ``zope.formlib`` for most of its forms: 
   <http://docs.zope.org/zope.formlib/>.
.. _GroupServer: http://groupserver.org/
