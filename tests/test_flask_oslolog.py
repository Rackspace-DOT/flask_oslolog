import os
from flask import Flask

from oslo_config import fixture
from testtools import TestCase

from flask_oslolog import OsloLog


class TestFlaskOslog(TestCase):

    def setUp(self):
        """
        Setup for Test Cases.

        Standard TestCase, setUp is run before each test. In this particular
        case, a basic flask app with this extension is instantiated.

        Logs are written to a temp file `self.test_log_file`, which is deleted
        after each test.
        """
        super(TestFlaskOslog, self).setUp()
        self.test_log_file = "test_flask_oslolog.log"
        self.conf = self.useFixture(fixture.Config())
        self.flask_app = Flask("test_flask_oslolog")
        self.log = OsloLog()
        self.conf.config(log_file=self.test_log_file)
        self.log.init_app(self.flask_app)

        self.app = self.flask_app.test_client()

        @self.flask_app.route("/test")
        def test_endpoint():
            """
            Simple test endpoint.

            Super simple endpoint used for testing logging of
            incoming requests.
            """
            return "success"

    def tearDown(self):
        """
        Counterpart to setUp.

        Standard TestCase tearDown, run after each test. In this case, simply
        removes the temp log file.
        """
        super(TestFlaskOslog, self).tearDown()
        os.remove(self.test_log_file)

    def test_instantiation(self):
        """Test that the "logger" is present for arbitrary use."""
        assert hasattr(self.log, "logger")

    def test_direct_app_presence(self):
        """
        Test that direct instantiation works as expected.

        setUp uses the application factory method, but standard direct
        instantiation should be available as well to comply with flask
        extension development rules.
        """
        log = OsloLog(self.flask_app)
        assert hasattr(log, "logger")

    def test_request_logging(self):
        """Test that a request is successfully logged to the log file."""
        self.app.get("/test")
        with open(self.test_log_file, 'r') as f:
            expected = ('INFO flask_oslolog.middleware [-] 127.0.0.1'
                        ' - - "GET /test" status: 200 len: 7')
            self.assertIn(expected, f.read(), "GET request not in test log.")

    def test_query_string_logging(self):
        """Test that query strings are similarly logged."""
        self.app.get("/test?athing=anotherthing")
        with open(self.test_log_file, 'r') as f:
            expected = "GET /test?athing=anotherthing"
            self.assertIn(expected, f.read(),
                          "GET querystring request not in test log.")

    def test_arbitrary_logging(self):
        """Test that the logger construct successfully writes to file."""
        self.log.logger.warn("This is a warning.")
