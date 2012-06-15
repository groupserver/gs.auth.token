Introduction
============

Token-authentication is used to allow server-side scripts to access forms
in `GroupServer`_. It simplest authentication method provided by the
system:

* The server-side scripts looks up token from the database.
* The token is passed in as part of the ``POST`` request that is made to
  submit the form.
* GroupServer checks the token with the one in the database, and throws a
  validation-error if they do not match.

.. _GroupServer: http://groupserver.org/
