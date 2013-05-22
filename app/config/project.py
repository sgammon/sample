# -*- coding: utf-8 -*-

"""
Config: Project

This file holds main project configuration.

:author: Sam Gammon (sam@momentum.io)
:copyright: (c) 2013 momentum labs.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""

"""

    ######################################## AppTools Project configuration. ########################################

    Main project configuration stuff, designed to be changed according to the app's desired environment and status.


"""

# stdlib
import os

config = {}


## App settings
config['apptools.project'] = {

    'name': 'Sample',            # Change this to your app's name

    'version': {               # Change this according to your app's version
        'major': 0,
        'minor': 1,
        'micro': 0,
        'build': 20130522,
        'release': 'ALPHA'
    }

}

## Development/debug settings
config['apptools.project.dev'] = {
  # Not yet in use
}

## Output layer settings
config['apptools.project.output'] = {

    # Output Configuration

    'debug': False,
    'minify': False,       # whether to minify page output or not
    'optimize': True,     # whether to use the async script loader or not
    'standalone': False,  # whether to render only the current template, or the whole context (ignores "extends")

    'analytics': {  # Analytics Settings
        'enable': False,              # whether to insert analytics code
        'multitrack': True,			 # whether to enable support for multiple trackers
        'anonymize': False,			 # whether to anonymize IPs before analytics
        'account_id': {
            'default': 'UA-XXX'   # main yoga analytics tracking
        },
        'sitespeed': {
            'enable': True,           # enable google analytics' site speed tracking
            'sample': 100            # set the sitespeed sample rate
        },
        'webclient': {
            'dev': 'https://ssl.google-analytics.com/u/analytics_debug.js',
            'http': 'https://ssl.google-analytics.com/u/analytics_debug.js',
            'https': 'https://ssl.google-analytics.com/u/analytics_debug.js'  # revert to: https://deliver.ampushyoga.io/ga.js
        }
    },

    'appcache': {  # HTML5 appcaching
        'enable': False,                       # whether to enable
        'manifest': 'scaffolding-v1.appcache'  # manifest to link to
    },

    'assets': {  # Asset API
        'minified': False,       # whether to switch to minified assets or not
        'serving_mode': 'local',  # 'local' or 'cdn' (CDN prefixes all assets with an absolute URL)
        'cdn_prefix': []  # CDN prefix/prefixes - a string is used globally, a list of hostnames is selected from randomly for each asset
    },

    'headers': {  # Default Headers (only supported headers are shown)
        'Vary': 'Content-Encoding',
        'Content-Language': 'en-US,en',
        'Cache-Control': 'private,max-age=3600',  # default to not caching dynamic content
        'X-Powered-By': 'Sample/v0.1-alpha',
        'X-UA-Compatible': 'IE=edge,chrome=1',  # http://code.google.com/chrome/chromeframe/
        'XAF-Origin': 'AppHosting/Sample/1.0',
        'Access-Control-Allow-Origin': None,
        'Access-Control-Allow-Methods': 'GET, POST',
        'Access-Control-Allow-Headers': 'Content-Type, Content-Length, XAF-Session, XAF-Token, XAF-Channel, XAF-Socket, X-ServiceTransport, X-ServiceClient',
        'Access-Control-Expose-Headers': 'Content-Type, Content-Length, XAF-Session, XAF-Token, XAF-Channel, XAF-Socket, X-ServiceTransport, X-ServiceClient'
    }

}

## Caching
config['apptools.project.cache'] = {

    # Caching Configuration

    'key_seperator': '::',
    'prefix': 'dev',
    'prefix_mode': 'explicit',
    'prefix_namespace': False,
    'namespace_seperator': '::',

    'adapters': {

        # Instance Memory
        'fastcache': {
            'default_ttl': 600
        },

        # Memcache API
        'memcache': {
            'default_ttl': 10800
        },

        # Backend Instance Memory
        'backend': {
            'default_ttl': 10800
        },

        # Datastore Caching
        'datastore': {
            'default_ttl': 86400
        }

    }

}

config['apptools.project.output.template_loader'] = {

    # Template Loader Config

    'force': True,              # Force enable template loader even on Dev server
    'debug': False,             # Enable dev logging
    'use_memory_cache': False,  # Use handler in-memory cache for template source
    'use_memcache': False,      # Use Memcache API for template source

}

# Pipelines Configuration
config['apptools.project.pipelines'] = {

    'debug': True,  # Enable basic serverlogs
    'logging': {

        'enable': False,       # Enable the pipeline logging subsystem
        'mode': 'serverlogs',  # 'serverlogs', 'xmpp' or 'channel'
        'channel': '',         # Default channel to send to (admin channels are their email addresses, this can be overridden on a per-pipeline basis in the dev console)
        'jid': '',             # Default XMPP JID to send to (this can be overridden on a per-pipeline basis in the dev console)

    }

}

# Models/Storage Configuration
config['apptools.model'] = {

    'debug': False,  # log messages
    'default': 'Memory',  # default storage engine

    'engines': [

        {'name': 'Redis', 'enabled': True, 'path': 'apptools.model.adapter.redis.Redis'},
        {'name': 'Memory', 'enabled': True, 'path': 'apptools.model.adapter.inmemory.InMemory'},
        {'name': 'Memcache', 'enabled': False, 'path': 'apptools.model.adapter.memcache.Memcache'}

    ]

}


# Redis Adapter
config['apptools.model.adapters.redis.Redis'] = {

    'debug': False,  # debug messages

    'servers': {

        'default': 'example',

        # Redis Instances
        'example': {'unix_socket_path': '/ns/runtime/sock/redis.sock', 'db': 5}

    }

}

# Memcache Adapter
config['apptools.model.adapters.memcache.Memcache'] = {

    'debug': True,  # debug messages

    'servers': {
        'local': {'host': '127.0.0.1', 'port': 11211, 'unix': '/ns/runtime/sock/memcache.sock'}
    }

}


config['apptools.classes.WebHandler'] = {

    'debug': False,
    'logging': True,

    'integrations': {

        'gravatar': {
            'enabled': False,
            'endpoints': {
                'http': 'www.gravatar.com',
                'https': 'secure.gravatar.com'
            }
        }

    },

    'extensions': {
        'load': ['FragmentCache', 'DynamicContent', 'MemcachedBytecodeCache']
    }

}

config['apptools.output.meta'] = {

    'icon': '<invalid>',
    'logo': '<invalid>',
    'author': 'momentum labs.',
    'publisher': 'momentum labs.',
    'copyright': 'momentum labs, (c) 2013',
    'robots': 'noindex,nofollow',  #'index,follow',
    'revisit': '7 days',

    'description': 'Sample apptools app for Ampush.',

    'application-name': 'ampush sample',
    'viewport': 'width=device-width,initial-scale=1,user-scalable=yes,height=device-height',
    'revisit-after': '7 days',

    'keywords': [
        'sample',
        'apptools',
        'wsgi'
    ],

    'opengraph': {

        'title': 'ampush sample: welcome',
        'type': 'website',
        'determiner': 'a',
        'locale': 'en_US',
        'url': 'https://sample.amp.sh',
        'site_name': 'project sample',
        'description': 'Sample apptools app for Ampush.',
        'image': '',

        'location': {
            'enable': True,

            'latitude': '',
            'longitude': '',
            'address': '450 9th Street, 2nd Floor',
            'locality': 'San Francisco',
            'region': 'California',
            'zipcode': '94103',
            'country': 'United States of America',
            'email': 'sample@ampush.com',
            'phone': ''
        },

        'facebook': {
            'app_id': '',
            'admins': ['642005650']
        }

    },

    'apple': {

        'touch_icon': '',
        'precomposed': '',
        'startup_icon': '',
        'status_bar_style': '',
        'app_capable': ''

    },

    'google': {

        'site_verification': ''

    }

}


## Platform config
config['platform.ampush.sample.Sample'] = {
    'debug': True,
    'coolsetting': 123
}


## Service config
config['coolapp.services.notes.NoteService'] = {
    'debug': True,
    'coolsetting2': 'blabs'
}
