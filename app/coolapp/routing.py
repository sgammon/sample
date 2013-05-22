# -*- utf-8 -*-

"""
API: Routes

This file contains API routing rules that pass requests
bound to certain URLs to the mapped handler.

:author: Sam Gammon (sam@momentum.io)
:copyright: (c) 2013 momentum labs.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

# webapp2
from webapp2 import Route
from webapp2_extras import routes


_VERSION_PREFIX = 'v1'


def get_rules():

    ''' Return URL routing rules. '''

    return [

        routes.HandlerPrefixRoute('coolapp.handlers.', [
            Route('/env', name='landing', handler='hello.Environment'),
            Route('/', name='landing', handler='hello.Landing')
        ])

    ]
