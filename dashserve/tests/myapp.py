import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from dashserve import JupyterDash

# example adopted from https://github.com/plotly/dash-docs/blob/master/tutorial/examples/getting_started.py
# the original code is Copyright (c) 2018 Plotly

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# this is the only change -- use JupyterDash() instead of Dash()
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),

    html.Div([
        dcc.Input(id='my-id', value='initial value', type='text'),
        html.Div(id='my-div')
    ])
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    global dsa
    dsa.logger.info('my message')
    return 'You\'ve entered "{}"'.format(input_value)

# Run the server
if __name__ == '__main__':
    app.run_server()