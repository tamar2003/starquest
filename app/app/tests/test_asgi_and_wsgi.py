import os
from django.test import TestCase

from app.asgi import application as asgi_application
from app.wsgi import application as wsgi_application


class ASGITestCase(TestCase):
    def test_asgi_application_loaded(self) -> None:
        """Ensure the ASGI application object is loaded and not None."""
        self.assertIsNotNone(asgi_application)

    def test_asgi_settings_configured(self) -> None:
        """Ensure DJANGO_SETTINGS_MODULE is correctly set for ASGI."""
        self.assertEqual(
            os.environ.get('DJANGO_SETTINGS_MODULE'),
            'app.settings'
        )


class WSGITestCase(TestCase):
    def test_wsgi_application_loaded(self) -> None:
        """Ensure the WSGI application object is loaded and not None."""
        self.assertIsNotNone(wsgi_application)

    def test_wsgi_settings_configured(self) -> None:
        """Ensure DJANGO_SETTINGS_MODULE is correctly set for WSGI."""
        self.assertEqual(
            os.environ.get('DJANGO_SETTINGS_MODULE'),
            'app.settings'
        )
