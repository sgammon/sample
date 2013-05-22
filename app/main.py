# -*- coding: utf-8 -*-

"""
This is where it all begins... ah, the wonderful *main.py*.
From here, we stitch together :py:mod:`apptools` and :py:mod:`gevent`
to provide an entrypoint for :py:mod:`apptools.dispatch`.

:author: Sam Gammon (sam@momentum.io)
:copyright: (c) 2013 momentum labs.
:license: This is private source code - all rights are reserved. For details about
          embedded licenses and other legalese, see `LICENSE.md`.
"""
__docformat__ = 'restructuredtext en'
__version__ = '0.5'

# stdlib / app
import os
import sys
import config
import bootstrap

# prepare sys.path
bootstrapper = bootstrap.AppBootstrapper.prepareImports()

# apptools, by momentum :)
import apptools

# apptools central dispatch
from apptools import dispatch

# uWSGI
try:
    import uwsgi; PLATFORM = 'uWSGI'
except ImportError as e:
    ## Not running from uWSGI.
    PLATFORM = 'WSGI'

# PyPy
try:
    import pypycore; RUNTIME = 'PyPy'
except ImportError as e:
    ## Not running in PyPy.
    RUNTIME = 'CPython'

# gevent
from gevent import local
from gevent import monkey

# Globals
_DEBUG = True  # DANGER: core debug flag, use with caution
_patched = False  # init flag for monkey patching via gevent
_locals = local.local()  # gevent greenlet local storage
_runcount = 0  # only used in debug: current count of profiler runs
sysconfig = config.config.get('apptools.system')

# Preload
bootstrapper.preload(_DEBUG)


def devserver(app=dispatch.gateway, port=config._DEVSERVER_PORT, host=config._DEVSERVER_HOST):

    ''' Start a local listener for development, using :py:mod:`gevent.pywsgi`.

        :param app:
            WSGI application to run. Defaults to :py:mod:`apptools.dispatch.gateway`.

        :param port:
            Port to run the application on. Defaults to the value of :py:attr:`config._DEVSERVER_PORT`,
            which is usually set to ``8080``.

        :param host:
            IP to bind the devserver to. Defaults to the value of :py:attr:`config._DEVSERVER_HOST`,
            which is usually set to ``127.0.0.1``. Setting this value to an empty string binds to
            all available IPs - *make sure it is not set to this in production*.

        .. note :: Dispatching this function from Python (or the command line) will block forever
                   via :py:meth:`pyuwsgi.WSGIServer.serve_forever`.

    '''

    global _locals
    global _patched
    global _runcount

    # mock devserver
    from gevent import pywsgi

    print "Starting listener for app %s on host/port %s:%s." % (app, host, port)

    if not _patched:
        # Patch stdlib for gevent
        monkey.patch_all()
        _patched = True

    prefix = os.path.abspath(__file__).split('/')[0:-2]

    if isinstance(app, (type(devserver), type)):
        appname = app.__name__
    else:
        appname = app.__class__.__name__

    if config.debug and sysconfig.get('hooks', {}).get('callgraph', {}).get('enabled', False):  # enable callgraph?

        try:
            import pycallgraph; _CALLGRAPH = True
        except ImportError:
            _CALLGRAPH = False
        else:
            print "Callgrapher enabled..."

        if _CALLGRAPH:

            ## define runnable that injects callgrapher
            def callgraphed_application(*args, **kwargs):

                ''' Start measuring the callgraph and dispatch. '''

                global _runcount

                # start tracing right before dispatch
                pycallgraph.start_trace()
                for chunk in app(*args, **kwargs):
                    yield chunk  # exhaust app generator

                # stop tracing after request is finished
                pycallgraph.stop_trace()
                _runcount = _runcount + 1
                pycallgraph.make_dot_graph('/'.join(prefix + ['.profile', '%s-%s-callgraph.png' % (appname, _runcount)]))
                raise StopIteration()

            application = callgraphed_application

    elif (config.debug and sysconfig.get('hooks', {}).get('profiler', {}).get('enabled', False)):  # enable profiler?

        print "Running devserver with profiler enabled..."

        # profiler + inspector
        try:
            import cProfile
            profile = cProfile
        except ImportError:
            import profile

        ## define runnable that injects profiler
        def profiled_application(*args, **kwargs):

            ''' Run application, instrumented with cProfile. '''

            global _runcount

            profiler = profile.Profile()

            # run with profiler, optionally tracing as we go
            for chunk in profiler.runcall(app, *args, **kwargs):
                yield chunk

            _runcount = _runcount + 1
            profiler.dump_stats('/'.join(prefix + ['.profile', '%s-%s.profile' % (appname, _runcount)]))
            print "Dumped profiler stats."
            raise StopIteration()

        application = profiled_application

    else:
        application = app  # no shim

    server = pywsgi.WSGIServer((host, port), application)
    server.serve_forever()

    print "Closed listener."
    exit(0)


## Handle full-listener debug spawn
if __name__ == "__main__":
    devserver(dispatch.gateway)
