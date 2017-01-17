Getting Started with Flask Oslo Log
=======================================

Flask Oslo Log is a Flask Extension which adds request logging via
:mod:`oslo.log`, as well as exposing an arbitrary logger to :mod:`oslo.log`
similarly to the standard app logger.

Configuring the Extension
-------------------------

:mod:`flask_oslolog` requires no configuration of it's own, but you may wish
to utilize the upstream configuration options of `oslo.log` to configure
log file location, etc.

A basic configuration might look like this:

.. code-block:: ini

    [DEFAULT]
    debug=True
    log_file=/var/log/yourapp/flask.log

Initializing the Extension
--------------------------

Simply wrap the application object during instantiation:

.. code-block:: python

   from flask import Flask

   from flask_oslolog import OsloLog

   app = Flask(__name__)
   log = OsloLog(app)

   if __name__ == "__main__":  # pragma: nocover
       app = create_app(app_name=__name__)
       app.run(host="0.0.0.0", port=5000

Accessing the extension
-------------------------

Once the extension is intialized, you will notice that, by default, request
logging has been enabled. In your log file you will begin to see messages
like this:

.. code-block:: text
2017-01-19 18:30:26.654 2082 INFO flask_oslog.middleware [-] 10.19.26.194 russ7612 Confirmed "GET /v1/prefab/1" status: 200 len: 8317

Additionally, arbitrary logging will become available:

.. code-block:: python

   from flask import Flask

   from flask_oslolog import OsloLog

   app = Flask(__name__)
   log = OsloLog(app)

   @app.route("/")
   log.logger.warn("Someone is accessing the root!")
   return "access granted"

   if __name__ == "__main__":  # pragma: nocover
       app = create_app(app_name=__name__)
       app.run(host="0.0.0.0", port=5000


Initializing the Extension in an Application Factory app
--------------------------------------------------------

As with all flask extensions, it is also accessible in an application Factory
setting by initializing the extension separately from it's instantiation:

.. code-block:: python

   from flask import Flask

   from flask_oslolog import OsloLog

   log = OsloLog()

   def create_app(app_name):
       app = Flask(app_name)
       log.init_app(app)

       return app


   if __name__ == "__main__":  # pragma: nocover
       app = create_app(app_name=__name__)
       app.run(host="0.0.0.0", port=5000)
