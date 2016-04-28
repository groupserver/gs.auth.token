=================
``gs.auth.token``
=================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Token authentication for GroupServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-06-18
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

Token-authentication is used to allow server-side scripts to
access forms in `GroupServer`_. It is the simplest authentication
method provided by the system:

* You create a token.
* You add authentication to a form.
* The token is passed in as part of the ``POST`` request that is
  made to submit the form.
* GroupServer checks the token with the one in the database, and
  throws a validation-error if they do not match.

This product provides both the API for checking the token, and
the ``console_script`` for generating a new token.

Resources
=========

- Documentation:
  http://groupserver.readthedocs.io/projects/gsauthtoken
- Code repository: https://github.com/groupserver/gs.auth.token/
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
