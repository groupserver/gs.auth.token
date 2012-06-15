Introduction
============

Token-authentication is used to allow server-side scripts to access forms
in `GroupServer`_. It is the simplest authentication method provided by the
system:

* The server-side scripts looks up token from the database.
* The token is passed in as part of the ``POST`` request that is made to
  submit the form.
* GroupServer checks the token with the one in the database, and throws a
  validation-error if they do not match.

Token Creation
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

.. _GroupServer: http://groupserver.org/
