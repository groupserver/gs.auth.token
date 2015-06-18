:mod:`gs.auth.token` API
========================

Using token authentication is normally done in two steps. First
the token is added to `the interface`_, and then used in `the
form`_.

The interface
-------------

The interface defines the parameters that the web hook
accepts. To use token authentication one of the parameters should
be an instance of the :class:`AuthToken` class.

.. class:: AuthToken(title, token, required)

   An authentication token field.

   :param str title: The title (almost always ``Token``)
   :param str description: The description of the field.
   :param bool required: Weather the field is required (almost
                         always ``True``)
   :raises AuthenticationTokenMismatch: There was a miss-match
      between the supplied token and the stored token.

   Web-hooks that want to use token authentication include a
   :class:`AuthToken` attribute as a parameter.

.. class:: AuthenticationTokenMismatch()

   The supplied token failed to match the token stored in the
   database.

Example
~~~~~~~

In the following example the ``ISomeHook`` interface class is
created with the ``token`` property set to be an instance of the
:class:`AuthToken` class.

.. code-block:: python

  from __future__ import unicode_literals
  from zope.interface.interface import Interface
  from gs.auth.token import AuthToken

  class ISomeHook(Interface):

      token = AuthToken(
          title='Token',
          description='The authentication token',
          required=True)

The form
--------

A form that actually supplies the web-hook uses `the interface`_,
and handles any errors using the :func:`log_auth_error` function.

.. function:: log_auth_error(context, request, errors)

   Log a token authentication error.

   :param context: The context of the current page (hook).
   :param request: The current request.
   :param errors: The errors that have occurred.

   This utility will check for the
   :class:`AuthenticationTokenMismatch` error in the list of
   ``errors``. If present it will add an audit-event to the
   audit-trail table.

Example
~~~~~~~

Typically the form that provides a web-hook is a subclass of the
JSON :class:`SiteEndpoint` class [#json]_. If there is an error
in the form then the utility :func:`gs.auth.token.log_auth_error`
should be called.

.. code-block:: python

    from zope.formlib import form
    from gs.auth.token import log_auth_error
    from gs.content.form.api.json import SiteEndpoint
    from .interfaces import ISomeHook


    class SomeHook(SiteEndpoint):
        '''The hook'''
        label = 'Some hook'
        form_fields = form.Fields(ISomeHook, render_context=False)

        @form.action(label='Some', name='some', prefix='',
                     failure='handle_some_failure')
        def handle_some(self, action, data):
            '''Do something

    :param action: The button that was clicked.
    :param dict data: The form data.'''

        def handle_some_failure(self, action, data, errors):
            log_auth_error(self.context, self.request, errors)
            retval = self.build_error_response(action, data, errors)
            return retval

.. [#formlib] GroupServer uses ``zope.formlib`` for most of its forms: 
   <http://docs.zope.org/zope.formlib/>.
.. [#json] See the ``gs.content.form.api.json`` product
           <https://github.com/groupserver/gs.content.form.api.json>
