import dash

from dashserve.server import JupyterDashServer


class JupyterDash(dash.Dash):
    """
    Drop-in replacement for dash.Dash to build applications in Jupyter Notebook

    Usage:
        app = JupyterDash(__name__) # use like dash.Dash()
        app.layout = ...
        app.run_server() # this is non-blocking so you can continue developing

        To add callbacks:

            @app.callback(...)
            def some_callback(...):
                return ...

        To interact with the Dash instance inside of a callback, e.g. output
        log messages, use the global dsa instead of the global app:

            def some_callback(...):
                global dsa
                dsa.logger.info('my log message')

        See DashserveApp for details.

        Note that the Dash app's stdout is tied to Jupyter's output area, so you can
        also use the normal print(...) statement for debugging.
    """

    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self._cbregistry = kwargs.get('cbregistry', [])
        self._name = name
        self.flask_server = self.server
        self.server = self._make_server()

    def _make_server(self):
        return JupyterDashServer(self)

    def callback(self, output, inputs=[], state=[]):
        """
        Wrapper to dash.Dash.callback to keep track of callback registrations

        See: dash.Dash.callback for details
        """
        wrapfunc = super().callback(output, inputs=inputs, state=state)

        def inner(func):
            cbtuple = func, output, inputs, state
            self._cbregistry.append(cbtuple)
            return wrapfunc(func)

        return inner

    def run_server(self, host='localhost', port=8050, **kwargs):
        """
        Runs a dash app from within Jupyter Notebook

        The app will be launched on given host and port and the log output
        will be sent back to Jupyter notebook.

        Note this is non-blocking so your notebook remains available for
        further work while the application is being served.
        """
        self.server.run(host=host, port=port, **kwargs)

    def stop(self):
        self.server.stop()

    def save(self, appfile):
        self.server.save(appfile)


class DashserveApp(dash.Dash):
    """
    Drop-in replacement for dash.Dash in served applications

    This is the class that DashAppSerializer will instantiate
    on deserializing an app to serve it. Currently a placeholder
    for easier future extensions.

    Within callbacks, an instance of DashserveApp is available
    as the global dsa.

    Usage:

        @app.callback(....)
        def mycallback(...):
            global dsa
            dsa.logger("some log message")

    Caution:
        Why not just use the global app? Because we don't serialize the
        global app in order to provide better stability. If you use the global
        app inside a callback, app.run_server() is likely to throw an error.

        Technically, the global app is tied to the Flask instance that
        exists in your Jupyter notebook. It's just not a good idea to serialize
        a full Flask app. So we don't.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # clean up log handlers (Dash always adds a handler even if it exists already,
        # however in Jupyter notebook served apps we can have many invocations)
        for hdlr in self.logger.handlers[:-1]:
            self.logger.removeHandler(hdlr)
