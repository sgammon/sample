# -*- coding: utf-8 -*-

'''
Sample handlers for a sample app!

:author: Sam Gammon (sam@momentum.io)
:copyright: (c) 2013 momentum labs.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

# stdlib
import os
import sys

# WebHandler
from coolapp.handlers import WebHandler


## Landing - homepage handler.
class Landing(WebHandler):

    ''' Sample landing page. '''

    def get(self):

        ''' HTTP GET
            :returns: Rendered template ``hello/world.html``. '''

        return self.render('hello/world.html')


## Environment - dumps request env.
class Environment(WebHandler):

    ''' Dumps request environment. '''

    def get(self):

        ''' HTTP GET
            :returns: Rendered template ``hello/env.html``. '''

        return self.render('hello/env.html')
