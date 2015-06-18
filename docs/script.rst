:program:`gs_auth_token_create`
===============================

.. program:: gs_auth_token_create

Synopsis
--------

   :program:`gs_auth_token_create` [:option:`-h`] :option:`dsn`

Description
-----------

:program:`gs_auth_token_create` creates a new token and adds it
to the relational database. Once run it is necessary to change
the `authentication configuration`_.

Positional arguments
--------------------

.. option:: dsn

   The data source name (DSN) in the form
   ``postgres://<user>:<password>@<host>:<port>/<database_name>``.
   The configuration file for GroupServer (normally
   ``etc/gsconfig.ini``) lists all the DSN entries for the
   system.

Optional arguments
------------------

.. option:: -h, --help

   Show a help message and exit

Returns
-------

* :program:`gs_auth_token_create` returns ``0`` on success and
  the new token is displayed on the standard output.
* ``1`` is returned if the system failed to make the initial
  connection to the database (the *engine* failed to be created).
* ``2`` is returned if the system failed to connect for any other
  reason.

Authentication Configuration
----------------------------

The scripts that use the web-hooks, such as :program:`smtp2gs`
[#smtp2gs]_, use the configuration file for storing the
token. :program:`gs_auth_token_create` leaves these configuration
files **unaltered,** because they can become complex. Instead it
displays the new token and the administrator must change the
entries in the configuration.

Examples
--------

Generate a new token and place it in the ``production``
database. In this example PostgreSQL is running on the default
port of the local machine — and has as been set up so
authentication is unnecessary:

.. code-block:: console

   $ gs_auth_token_create posgres://localhost/production

Generate a new token and place it in the ``testing`` database on
a *remote* machine ``groups.example.com`` — with the port
``5432`` explicitly passed. Authentication is used.

.. code-block:: console

   $ gs_auth_token_create \
     posgres://databaseUser:secretPass@groups.example.com:5432/testing

.. [#smtp2gs] See ``gs.group.messages.add.smtp2gs`` 
            <https://github.com/groupserver/gs.group.messages.add.smtp2gs>
