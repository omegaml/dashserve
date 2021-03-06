.. dashserve documentation master file, created by
   sphinx-quickstart on Sat Mar 30 15:57:52 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2

dashserve: Plotly Dash Served Easily
====================================

*dashserve* supports developing and serving Plotly Dash apps within Jupyter Notebook.
dashserve can also serialize Dash apps and serve them anywhere from a file.

What makes dashserve awesome?

* it takes just a single simple change to your existing Dash app (change :code:`dash.Dash` to :code:`JupyterDash`)
* serve straight from Jupyter Notebook or JupyterLab
* publish Dash apps in a standalone server
* no dependencies other than Plotly Dash (ok, some dill for serialization)

Installation
------------

.. code::

   $ pip install dashserve

Run from within Jupyter Notebook or Jupyter Lab
-----------------------------------------------

.. code:: python

   # in Jupyter Notebook
   from dashserve import JupyterDash

   app = JupyterDash(__name__)
   app.layout = ...
   app.run_server()

   * Serving Flask app "__main__" (lazy loading)
   * Environment: production
     WARNING: Do not use the development server in a production environment.
     Use a production WSGI server instead.
   * Debug mode: off
   * Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)

Run as a standalone server
--------------------------

Running a standalone server is just as easy

1. Save the JupyterDash app to a file

   .. code:: python

      # in Jupyter notebook
      app.save('/path/to/myapp.dash')

2. Run dashserve

   .. code:: bash

      # from the command line
      $ python -m dashserve /path/to/myapp.dash
      dashserve (c) 2019 one2seven GmbH, makers of omegaml.io - productize your AI/ML applications
       * Serving Flask app "__main__" (lazy loading)
       * Environment: production
         WARNING: Do not use the development server in a production environment.
         Use a production WSGI server instead.
       * Debug mode: off
       * Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)

Run as a production server
--------------------------

If you need to run in a production environment, use a WSGI server

.. code:: bash

   $ DASH_APP=/path/to/myapp.dash gunicorn dashserve.wsgi:app -b localhost:8050
   [2019-03-30 17:11:41 +0100] [19727] [INFO] Starting gunicorn 19.7.1
   [2019-03-30 17:11:41 +0100] [19727] [INFO] Listening at: http://127.0.0.1:8050 (19727)
   [2019-03-30 17:11:41 +0100] [19727] [INFO] Using worker: sync
   [2019-03-30 17:11:41 +0100] [19731] [INFO] Booting worker with pid: 19731


Build Powerful Machine Learning Apps
====================================

dashserve is an extension to `omega|ml`_, our core product to productize data science

Looking for a way to build & deploy machine learning apps with a single line of code?
Look no further. Just combine dashserve with omega|ml. Then you can integrate machine
learning models in Plotly Dash apps as easily as this:

.. code::

   app = JupyterDash(...)

   @app.callback(...)
   def prediction_output(input_value):
      model = om.models.get('mymodel')
      yhat = model.predict(input_value)
      return 'prediction yhat={}'.format(yhat)

Getting data from omega|ml is also just one line of code:

.. code::

   # in your Dash app
   import omegaml as om
   df = om.datasets.get('mydata')

   # see https://dash.plot.ly/getting-started, Reusable components for a full example

Publishing data and the trained model directly from Jupyter is straight forward - it's literally
just two lines of code. Here's a full example:

.. code::

   # in your jupyter notebook (model training)
   from sklearn import datasets
   from sklearn import svm
   import omegaml as om

   iris = datasets.load_iris()

   # train model
   clf = svm.SVC(gamma='scale')
   X, y = iris.data, iris.target
   clf.fit(X, y)

   # save model and data
   om.datasets.put(iris, 'mydata')
   om.models.put(clf, 'mymodel')


Dependencies
============

dashserve supports Plotly Dash version 0.39 or later. It uses the dill package
by Mike McKerns to serialize applications. Requires Python 3.6 or later.

Why dashserve?
==============

We looked at several other options, however found none matched our needs: to develop
Plotly Dash apps using Jupyter Notebook or JupyterLab and deploy them later.

* https://pypi.org/project/jupyter-plotly-dash/ requires Django while Dash depends on Flask.
  Mixing two web frameworks adds too much complexity and does not sound like a good idea
  in the first place.

* https://github.com/plotly/jupyterlab-dash is a JuypterLab extension. That's nice if you
  run JupyterLab, however it does not support serialized apps and serve from another server.

License
=======

The MIT License (MIT)

Copyright (c) 2019 one2seven GmbH, makers of omega|ml, http://omegaml.io

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Commercial support
==================

dashserve is brought to you by omega|ml - productize machine learning

The commercial version of dashserve is a module of omega|ml to provide multi-user
analytics dashboards, enterprise-grade security, full data integration and machine
learning applications. From laptop to web scale, all deployed with a single-line of code.

We can help you build and deploy analytics applications easily. Get in touch
at info@omegaml.io or chat with us at http://omegaml.io

* Serving machine learning models to applications using our state-of-the art REST API
* Getting your data science team from zero to speed using omega|ml, batteries included
* Consulting on data science, visualizations using Plotly and machine learning frameworks



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _omega|ml: https://omegaml.io

