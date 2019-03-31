from logging import warning
from multiprocessing import Process

from dashserve.serializer import DashAppSerializer


def runner(serialized_app, host, port, **kwargs):
    serializer = DashAppSerializer()
    app = serializer.deserialize(serialized_app)
    app.run_server(host=host, port=port, **kwargs)


class JupyterDashServer:
    """
    Dash Server to run a JupyterDash app in a separate process
    """
    __SERVERS = []

    def __init__(self, app, host='localhost', port=8050):
        self.app = app
        self.runner = None
        self.host = host
        self.port = port

    def run(self, host=None, port=None, debug=False, **kwargs):
        host = host or self.host
        port = port or self.port
        # stop previous servers before we relaunch
        self.stop_servers()
        # launch a new server
        serialized_app = self.serializer.serialize(wrap=False)
        runner_args_tuple = (serialized_app, host, port)
        if debug:
            warning('*** debug=True is not yet supported')
        self.runner = Process(target=runner, args=runner_args_tuple, kwargs=kwargs)
        self.runner.start()
        # register so we can later stop. note this will survive creating new instances by use of class.SERVERS
        self.register()
        return self

    def register(self):
        if self not in JupyterDashServer.__SERVERS:
            JupyterDashServer.__SERVERS.append(self)

    def stop_servers(self):
        for server in JupyterDashServer.__SERVERS:
            server.stop()

    def stop(self):
        if self.runner:
            self.runner.terminate()
            self.runner = None
            JupyterDashServer.__SERVERS.remove(self)
        print("Stopped")

    def update(self, app):
        self.runner.stop()
        self.app = app
        self.run()

    @property
    def serializer(self):
        return DashAppSerializer(self.app)

    def save(self, appfile):
        serialized = self.serializer.serialize(wrap=False)
        with open(appfile, 'wb') as fout:
            app = fout.write(serialized)


class SerializedDashServer:
    def __init__(self, serialized_app, host='localhost', port=8050):
        self.serialized_app = serialized_app
        self.host = host
        self.port = port

    def run(self, host=None, port=None):
        host = host or self.host
        port = port or self.port
        runner(self.serialized_app, host, port)

    def as_wsgi(self):
        serializer = DashAppSerializer()
        app = serializer.deserialize(self.serialized_app)
        return app.server

    @classmethod
    def from_file(cls, appfile, host=None, port=None):
        with open(appfile, 'rb') as fin:
            serialized = fin.read()
        return SerializedDashServer(serialized, host=host, port=port)
