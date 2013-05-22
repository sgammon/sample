# -*- coding: utf-8 -*-

'''
API: Services

This package exports classes for use as ProtoRPC services. Services defined
here and registered in config at `config.services` will automatically appear
(unless hidden) in the JavaScript context.

The AppTools service layer is integrated with AppTools JS and uses a simple,
custom JSON-wire format to dispatch RPC services. ProtoRPC (the underlying
plumbing for API dispatch and serialization) allows compatibility outside
of standard HTTP scope - so, service methods could theoretically be dispatched
over WebSockets or other exotic transports without code changes.

The services listed here are dependent on Message classes, that structure
the Request/Response flow. AppTools models happen to make great Message classes.
Messages that must be custom-built live in `messages`.

:author: Sam Gammon (sam@momentum.io)
:copyright: (c) 2013 momentum labs.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Base Imports
import config
import webapp2

# apptools services
from apptools import services

# apptools util
from apptools.util import debug


## APIService - abstract parent for all service APIs
class APIService(services.BaseService):

    ''' Abstract parent class for all API services. '''

    @webapp2.cached_property
    def config(self):

        ''' Cached access to `SampleService` config. '''

        return config.config.get(self._config_path, {'debug': False})

    @webapp2.cached_property
    def logging(self):

        ''' Cached access to dedicated log pipe. '''

        path = self._config_path.split('.')
        return debug.AppToolsLogger(path='.'.join(path[0:-1]), name=path[-1])._setcondition(self.config.get('debug'))
