from tempfile import gettempdir
from time import sleep
from unittest import TestCase

import os
import requests
from subprocess import Popen

from dashserve.serializer import DashAppSerializer
from dashserve.server import SerializedDashServer
from dashserve.tests import myapp


class DashServeTests(TestCase):
    def setUp(self):
        self.app = myapp.app

    def tearDown(self):
        pass

    def test_serializer(self):
        app = self.app
        serializer = DashAppSerializer(self.app)
        serialized = serializer.serialize()
        new_app = serializer.deserialize(serialized)
        # see if attributes were restored
        self.assertEqual(new_app._external_stylesheets, app._external_stylesheets)
        # see if the callback map was restored
        for k, v in app.callback_map.items():
            self.assertIn(k, new_app.callback_map)
            for ki, vi in v.items():
                self.assertIn(ki, v)
                if ki != 'callback':
                    self.assertEqual(vi, new_app.callback_map[k][ki])
                else:
                    self.assertEqual(vi.__name__, new_app.callback_map[k][ki].__name__)

    def test_jupyter_server(self):
        app = self.app
        app.run_server(port=8199)
        sleep(2)
        resp = requests.get('http://localhost:8199')
        app.stop()

    def test_standalone_server(self):
        app = self.app
        fn = os.path.join(gettempdir(), 'testapp.dash')
        app.save(fn)
        p = Popen('python -m dashserve {fn} -P 8199'.format(**locals()).split(' '))
        sleep(5)
        resp = requests.get('http://localhost:8199')
        p.terminate()
        p.wait()





