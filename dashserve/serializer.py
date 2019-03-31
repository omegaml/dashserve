from base64 import b64encode, b64decode

from dill import dumps, loads

class DashAppSerializer:
    def __init__(self, app=None):
        self.app = app

    def serialize(self, wrap=True):
        app = self.app
        buffer = {
            'version': '0.1',
            'attrs': {
                'layout': app.layout,
                'css': app.css,
                'scripts': app.scripts,
                'config': app.config,
            },
            'args': [app._name],
            'kwargs': {
                'external_stylesheets': app._external_stylesheets,
                'external_scripts': app._external_scripts,
                'static_folder': app.flask_server.static_folder,
                'assets_folder': app._assets_folder,
                'assets_url_path': app._assets_url_path,
                'url_base_pathname': app.url_base_pathname,
                'index_string': app.index_string,
                'meta_tags': app._meta_tags,
                'assets_ignore': app.assets_ignore,

            },
            'rebuild': {
                'cbregistry': getattr(app, '_cbregistry', None),
            }
        }
        serialized = b64encode(dumps(buffer))
        if wrap:
            serialized = {
                'data': serialized
            }
        return serialized

    def deserialize(self, serialized):
        from dashserve.jupyter import DashserveApp

        if isinstance(serialized, dict):
            serialized = serialized['data']
        buffer = loads(b64decode(serialized))
        # re create dashappp
        # -- instantiate with kwargs
        app = DashserveApp(*buffer['args'], **buffer['kwargs'])
        # -- apply attributes
        for k, v in buffer['attrs'].items():
            setattr(app, k, v)
        # -- register call backs
        cbregistry = buffer['rebuild'].get('cbregistry', [])
        self._apply_callbacks(app, cbregistry)
        return app

    def _apply_callbacks(self, dsapp, cbregistry):
        for func, output, inputs, state in cbregistry:
            func.__globals__['dsa'] = dsapp
            dsapp.callback(output, inputs, state)(func)

