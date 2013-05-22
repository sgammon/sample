# -*- coding: utf-8 -*-

'''
App Config

This directory holds all of your apps' configuration info. AppTools can stitch together multiple config
files, as long as they export a `config` dictionary (add config files below in `apptools.system.include`...).

AppTools ships with a few other config files in this folder.

:author: Sam Gammon (sam@momentum.io)
:copyright: (c) 2013 momentum labs.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
'''

import os
import sys
import logging

try:
    import bootstrap

    if 'lib' not in sys.path or 'lib/distlib' not in sys.path:
        bootstrap.AppBootstrapper.prepareImports()

except ImportError as e:
    pass  # we don't care if the bootstrapper can't be found/can't run


## Globals
_config = {}
_compiled_config = None

## Check if we're running on top of the appengine devserver
force_debug = False  # toggle debug mode
strict = False  # toggle strict mode
verbose = True  # toggle verbose logging
production = (os.environ.get('APPFACTORY') == 'production') or (os.environ.get('SERVER_SOFTWARE', 'Not Google').startswith('Google'))
debug = force_debug or (not production)

## App details
appname = 'ampush-sample'
appversion = '0-1-alpha'

## Devserver config
_DEVSERVER_PORT = 8080
_DEVSERVER_HOST = '127.0.0.1'


"""

    ######################################## Webapp2 configuration. ########################################


"""

_config['webapp2'] = {

    'apps_installed': [
        'coolapp'  # Installed projects
    ],

}

_config['webapp2_extras.sessions'] = {

    'secret_key': '__CHANGEME__',
    'default_backend': 'securecookie',
    'cookie_name':     'amps',
    'session_ttl':     172000000,
    'session_max_age': None,
    'cookie_args': {
        'name':       'aps',
        'max_age':     172000000,
        #'domain':      '*',
        'path':        '/'
        #'secure':      False,
        #'httponly':    False
    },
    'require_valid': True

}

_config['webapp2_extras.jinja2'] = {

    'template_path': 'templates/source',  # Root directory for template storage
    'compiled_path': 'templates.compiled',  # Compiled templates directory
    'force_compiled': False,  # Force Jinja to use compiled templates, even on the Dev server

    'environment_args': {  # Jinja constructor arguments
        'optimized': True,   # enable jinja2's builtin optimizer (recommended)
        'autoescape': True,  # Global Autoescape. BE CAREFUL WITH THIS.
        'trim_blocks': False,  # Trim trailing \n's from blocks.
        'auto_reload': True,  # Auto-reload templates every time.
        'extensions': ['jinja2.ext.autoescape', 'jinja2.ext.with_', 'jinja2.ext.loopcontrols'],
    }

}


"""

    ######################################## Core configuration. ########################################

    Core system configuration, including settings for the WSGI app, config files, and installed Platforms.

"""

## System Config
_config['apptools'] = {}
_config['apptools.system'] = {

    'debug': False,  # System-level debug messages

    'config': {
        'debug': False  # configuration debug
    },

    'hooks': {  # System-level Developer's Hooks
        'appstats': {'enabled': False},  # AppStats RPC optimization + analysis tool
        'apptrace': {'enabled': False},  # AppTrace memory usage optimization + analysis tool
        'callgraph': {'enabled': False},  # Use `pycallgraph` to generate an image callgraph of the WSGI app
        'profiler': {'enabled': False}   # Python profiler for CPU cycle/efficiency optimization + analysis
    },

    'include': [  # Extended configuration files to include

        ('layer9', 'config.appfactory'),      # Layer9 Hosting Config
        ('extensions', 'config.extensions'),  # extension config
        ('project', 'config.project'),        # Base Project config
        ('services', 'config.services'),      # Global + site services (RPC/API) config
        ('assets', 'config.assets'),          # Asset manangement layer config
        ('middleware', 'config.middleware'),  # Config for service and handler middleware.

    ]

}

## Platform Config
_config['apptools.system.platform'] = {

    'installed_platforms': [

        {'name': 'Generic WSGI', 'path': 'apptools.platform.generic.GenericWSGI'},
        {'name': 'Layer9 AppFactory', 'path': 'apptools.platform.appfactory.AppFactory'},
        #{'name': 'AmpushSample', 'path': 'coolapp.platform.sample.SamplePlatform'},

    ]

}



"""
###    === Don't modify below this line... ===
"""


def systemLog(message, _type='debug'):

    ''' Logging shortcut. '''

    global debug
    global _config
    if _config['apptools.system']['debug'] is True or _type in ('error', 'critical'):
        prefix = '[CORE_SYSTEM]: '
        if _type == 'debug' or debug is True:
            logging.debug(prefix + message)
        elif _type == 'info':
            logging.info(prefix + message)
        elif _type == 'error':
            logging.error(prefix + message)
        elif _type == 'critical':
            logging.critical(prefix + message)


def readConfig(config=_config):

    ''' Parses extra config files and combines into one global config. '''

    global _compiled_config
    from webapp2 import import_string
    if _compiled_config is not None:
        return _compiled_config
    else:
        if config['apptools.system'].get('include', False) is not False and len(config['apptools.system']['include']) > 0:
            systemLog('Considering system config includes...')
            for name, configpath in config['apptools.system']['include']:
                systemLog('Checking include "' + str(name) + '" at path "' + str(configpath) + '".')
                try:
                    loaded_config = import_string('.'.join(configpath.split('.') + ['config']))
                    config.update(loaded_config)
                except Exception, e:
                    systemLog('Encountered exception of type "' + str(e.__class__) + '" when trying to parse config include "' + str(name) + '" at path "' + str(configpath))
                    if debug:
                        raise
                    else:
                        continue
        if len(config) > 0 and _compiled_config is None:
            _compiled_config = config

        return config

## Export compiled app config
config = readConfig(_config)
