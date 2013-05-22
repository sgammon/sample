# -*- coding: utf-8 -*-

'''
Sample API: Service

:author: Sam Gammon (sam@momentum.io)
:copyright: (c) 2013 momentum labs.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# apptools services
from apptools import model
from apptools import services

# apptools util
from apptools.util import datastructures

# base service
from coolapp.services import exceptions
from coolapp.services import APIService


## Error
# Generic error message.
class OhNoezError(exceptions.Error):

    ''' Raised when something went wrong. '''

    pass


## Echo
# Sample message.
class Echo(model.Model):

    ''' Sample model => message. '''

    message = basestring, {'default': 'Hello, world!'}


## NoteService - exposes methods for managing notes.
@services.api
class NoteService(APIService):

    ''' Exposes methods for managing ``Notes``. '''

    name = 'notes'
    _config_path = 'coolapp.services.notes.NoteService'

    exceptions = datastructures.DictProxy(**{
        'ohnoez': OhNoezError
    })

    @services.rpcmethod(Echo)
    def echo(self, request):

        ''' Echo back what we get. '''

        if request.message:
            return Echo(message=request.message)
        return Echo()
