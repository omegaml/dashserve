dashserve: Plotly Dash Served Easily
====================================

*dashserve* supports developing and serving Plotly Dash apps within Jupyter Notebook.
dashserve can also serialize Dash apps and serve them anywhere form a file.

Documentation https://omegaml.github.io/dashserve/html/index.html

Run from within Jupyter Notebook or Jupyter Lab
-----------------------------------------------

.. code::

   # in Jupyter Notebook
   from dashserve import JupyterDash

   app = JupyterDash(__name__)
   app.layout = html.Div(children=[
      ...
   ]
   app.run_server()

   * Serving Flask app "__main__" (lazy loading)
   * Environment: production
     WARNING: Do not use the development server in a production environment.
     Use a production WSGI server instead.
   * Debug mode: off
   * Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)

More options are available, see documentation

License
-------

dashserve is MIT licensed. Details see LICENSE file

Note Plotly Dash is Copyright (c) 2018 Plotly Inc, and is not part of dashserve

Commercial options
------------------

dashserve is brought to you by omega|ml - productize machine learning

The commercial version of dashserve is a module of omega|ml to provide multi-user
analytics dashboards, enterprise-grade security, full data integration and machine
learning applications. From laptop to web scale, all deployed with a single-line of code.

We can help you build and deploy analytics applications easily. Get in touch
at info@omegaml.io or chat with us at http://omegaml.io

* Serving machine learning models to applications via a state-of-the art REST API
* Getting your data science team from zero to speed using omega|ml, batteries included
* Consulting on data science, visualizations using Plotly and machine learning