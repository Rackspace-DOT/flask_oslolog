# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Flask-OsloLog adds logging via oslo.log to Flask.

No configuration is necessary for this extension outside of the standard
`oslo.log` configuration done via `oslo.config`. This extension will by
default use the following format:

'%(REMOTE_ADDR)s %(REMOTE_USER)s %(REMOTE_STATUS)s '
              '"%(REQUEST_METHOD)s %(REQUEST_URI)s" status: %(status)s'
              ' len: %(bytes)s'

Example:
2017-01-19 18:30:26.654 2082 INFO flask_oslolog.middleware [-] 10.19.26.194 \
 russ7612 Confirmed "GET /v1/prefab/1" status: 200 len: 8317

    REMOTE_ADDR:   Standard remote_addr header.
    REMOTE_USER:   If using keystone middleware, this will map to X-User-Id
    REMOTE_STATUS: If using keystone middleware, this will map to
                   X-Identity-Status
    REMOTE_METHOD: REST method (GET/PUT/POST/DELETE, etc.)
    REQUEST_URI:   endpoint uri, including query string.
    status:        response status code.
    len:           response byte length.
"""

from oslo_config import cfg
from oslo_log import log as logging

from flask_oslolog import middleware


__version__ = "0.1"


class OsloLog(object):

    def __init__(self, app=None):
        """
        Initialize app utilizing a flask app.

        :param app: `flask.Flask` application to extend.
        :type app: :py:class:`flask.Flask`

        supports optionally passing the app directly when not using the
        application factory style of Flask deployment.

        .. code-block: python

           from flask import Flask
           from flask_oslolog import OsloLog

           app = Flask(__name__)
           log = OsloLog(app)

        """
        self.app = app
        logging.register_options(cfg.CONF)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Support application factory style initialization.

        :param app: `flask.Flask` application to extend.
        :type app: :py:class:`flask.Flask`

        Instantiate OsloLog, and later apply to an application:

        .. code-block: python

           from flask import Flask
           from flask_oslolog import OsloLog

           log = OsloLog()

           app = Flask(__name__)
           log.init_app(app)
        """
        logging.set_defaults(
            default_log_levels=(logging.get_default_log_levels() +
                                ["flask=INFO", "werkzeug=INFO"]))
        logging.setup(cfg.CONF, app.name)
        self.logger = logging.getLogger(__name__)
        app.wsgi_app = middleware.OsloLogMiddleware(app.wsgi_app)
