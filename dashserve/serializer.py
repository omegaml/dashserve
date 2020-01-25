from base64 import b64encode, b64decode

from dill import dumps, loads

class DashAppSerializer:
    def __init__(self, app=None):
        self.app = app

    def serialize(self, wrap=True):
        app = self.app
        buffer = {
            'version': '1.0',
            'attrs': {
                'layout': app.layout,
                'css': app.css,
                'scripts': app.scripts,
                # 'config': app.config, # config should be only set through kwargs
            },
            'args': [app._name],
            'kwargs': {
                'external_stylesheets': app.config.external_stylesheets,
                'external_scripts': app.config.external_scripts,
                'assets_folder': app.config.assets_folder,
                'assets_url_path': app.config.assets_url_path,
                'url_base_pathname': app.config.url_base_pathname,
                'index_string': app.index_string,
                'meta_tags': app.config.meta_tags,
                'assets_ignore': app.config.assets_ignore,

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

    def deserialize(self, serialized, **kwargs):
        from dashserve.jupyter import DashserveApp

        if isinstance(serialized, dict):
            serialized = serialized['data']
        buffer = loads(b64decode(serialized))
        # re create dashappp
        # -- instantiate with kwargs
        buffer['kwargs'].update(kwargs)
        app = DashserveApp(*buffer['args'], **buffer['kwargs'])
        # -- apply attributes
        for k, v in buffer['attrs'].items():
            if k == 'config':
                # config should only be influenced by kwargs
                continue
            setattr(app, k, v)
        # -- register call backs
        cbregistry = buffer['rebuild'].get('cbregistry', [])
        self._apply_callbacks(app, cbregistry)
        return app

    def _apply_callbacks(self, dsapp, cbregistry):
        for func, output, inputs, state in cbregistry:
            func.__globals__['dsa'] = dsapp
            dsapp.callback(output, inputs, state)(func)

