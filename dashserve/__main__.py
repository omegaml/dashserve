import argparse

from dashserve.server import SerializedDashServer

print("dashserve (c) 2019 one2seven GmbH, makers of omegaml.io - productize your AI/ML applications")

parser = argparse.ArgumentParser(description='Serve a serialized dash app')
parser.add_argument('path', type=str, help='/path/to/file.dash')
parser.add_argument('--host', '-H', type=str, help='host, defaults to localhost', default='localhost')
parser.add_argument('--port', '-P', type=int, help='port, defaults to 8050', default=8050)

args = parser.parse_args()

server = SerializedDashServer.from_file(args.path)
server.run(host=args.host, port=args.port)
