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
            'args': [],
            'kwargs': {
                k: app.config.get(k) for k in app.config.keys()
            },
            'rebuild': {
                'cbregistry': getattr(app, '_cbregistry', None),
            }
        }
        # fix for duplicate name arguments in Dash > 1.6
        if 'name' not in buffer['kwargs']:
            buffer['kwargs']['name'] = app._name
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
        # fixing url_base_pathname and requests_pathname_prefix ambiguity
        # https://github.com/plotly/dash/issues/364
        if 'url_base_pathname' in buffer['kwargs']:
            del buffer['kwargs']['requests_pathname_prefix']
            del buffer['kwargs']['routes_pathname_prefix']
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

