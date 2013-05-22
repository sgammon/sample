# -*- coding: utf-8 -*-

'''
API Services: Exceptions

:author: Sam Gammon (sam@momentum.io)
:copyright: (c) 2013 momentum labs.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# Hermes Exceptions
from protorpc import remote


## Error - generic top-level exception for all `APIService` errors.
class Error(remote.ApplicationError): ''' Root, abstract `APIService` error class. '''
