# -*- coding: utf-8 -*-

'''
This package contains platform-specific code for Hermes, and
is the primary location for app-wide business logic.

:author: Sam Gammon (sam@momentum.io)
:copyright: (c) 2013 momentum labs.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Base Imports
import webapp2

# Platform Parent
from coolapp.platform import Platform


## Sample - version one of the `Sample` platform.
class Sample(Platform):

    ''' Version 1 of `Sample` platform. '''

    # Class Constants
    _config_path = 'platform.ampush.sample.Sample'

    @classmethod
    def check_environment(cls, environ, config):

        ''' Check if the current environment supports Tantric.

            :param environ: Current non-runtime environment ``dict``.
            :param config: System-wide configuration ``dict``.
            :returns: Boolean indicating whether this ``Platform``
                      should be loaded. '''

        return True

    @webapp2.cached_property
    def shortcut_exports(self):

        ''' Return shortcuts.
            :returns: List of ``(<name>, <obj>)`` pairs to create
                      shortcuts on target base classes for. '''

        # Shortcut exports
        return [
            ('hermes', self)
        ]

    @webapp2.cached_property
    def template_context(self):

        ''' Inject Tracker-specific template context.
            :returns: Callable function :py:func:`inject_tracker`,
                      which can be deferred until template
                      construction time, and returns context
                      mutations for this particular ``Platform``. '''

        def inject_context(handler, context):

            ''' Protocol/platform stuff.

                :param handler: The currently-active descendent of
                                :py:class:`webapp2.RequestHandler`.

                :param context: Template context ``dict`` to be
                                optionally mutated and returned.

                :returns: Materialized context ``dict``. '''

            return context

        return inject_context

    ## == Dispatch Hooks == ##
    def pre_dispatch(self, handler):

        ''' Invoked right before handler dispatch.

            :param handler: The currently-active descendent of
                            :py:class:`webapp2.RequestHandler`.

            :returns: The very same ``handler``, post-mutation. '''

        return handler

    def post_dispatch(self, handler, response):

        ''' Invoked right after handler dispatch.

            :param handler: The currently-active descendent of
                            :py:class:`webapp2.RequestHandler`.

            :returns: Nothing, the return value from this method is
                      **discarded**, since the response has already
                      been relayed to the requesting party. '''

        return
