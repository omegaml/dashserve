import os

from dashserve.server import SerializedDashServer

server = SerializedDashServer.from_file(os.environ['DASH_APP'])
app = server.as_wsgi()
