"""Unit tests for runners."""

from unittest.mock import patch

import pytest

from ols.app.models.config import Config
from ols.runners.uvicorn import start_uvicorn


@pytest.fixture
def default_config():
    """Fixture providing default configuration."""
    return Config(
        {
            "llm_providers": [],
            "ols_config": {
                "default_provider": "test_default_provider",
                "default_model": "test_default_model",
                "conversation_cache": {
                    "type": "memory",
                    "memory": {
                        "max_entries": 100,
                    },
                },
                "logging_config": {
                    "app_log_level": "error",
                },
                "query_validation_method": "disabled",
                "certificate_directory": "/foo/bar/baz",
                "authentication_config": {"module": "foo"},
            },
            "dev_config": {"disable_tls": "true"},
        }
    )


def test_start_uvicorn(default_config):
    """Test the function to start Uvicorn server."""
    # don't start real Uvicorn server
    with patch("uvicorn.run") as mocked_run:
        start_uvicorn(default_config)
        mocked_run.assert_called_once_with(
            "ols.app.main:app",
            host="0.0.0.0",  # noqa: S104
            port=8080,
            workers=1,
            log_level=30,
            ssl_keyfile=None,
            ssl_certfile=None,
            ssl_keyfile_password=None,
            ssl_version=17,
            ssl_ciphers="TLSv1",
            access_log=False,
        )


def test_start_uvicorn_with_tls(default_config):
    """Test the function to start Uvicorn server."""
    default_config.dev_config.disable_tls = False
    # don't start real Uvicorn server
    with patch("uvicorn.run") as mocked_run:
        start_uvicorn(default_config)
        mocked_run.assert_called_once_with(
            "ols.app.main:app",
            host="0.0.0.0",  # noqa: S104
            port=8443,
            workers=1,
            log_level=30,
            ssl_keyfile=None,
            ssl_certfile=None,
            ssl_keyfile_password=None,
            ssl_version=17,
            ssl_ciphers="TLSv1",
            access_log=False,
        )


def test_start_uvicorn_on_localhost(default_config):
    """Test the function to start Uvicorn server."""
    default_config.dev_config.run_on_localhost = True
    # don't start real Uvicorn server
    with patch("uvicorn.run") as mocked_run:
        start_uvicorn(default_config)
        mocked_run.assert_called_once_with(
            "ols.app.main:app",
            host="localhost",
            port=8080,
            workers=1,
            log_level=30,
            ssl_keyfile=None,
            ssl_certfile=None,
            ssl_keyfile_password=None,
            ssl_version=17,
            ssl_ciphers="TLSv1",
            access_log=False,
        )


def test_start_uvicorn_on_non_default_port(default_config):
    """Test the function to start Uvicorn server on a non-default port."""
    default_config.dev_config.uvicorn_port_number = 8081
    # don't start real Uvicorn server
    with patch("uvicorn.run") as mocked_run:
        start_uvicorn(default_config)
        mocked_run.assert_called_once_with(
            "ols.app.main:app",
            host="0.0.0.0",  # noqa: S104
            port=8081,
            workers=1,
            log_level=30,
            ssl_keyfile=None,
            ssl_certfile=None,
            ssl_keyfile_password=None,
            ssl_version=17,
            ssl_ciphers="TLSv1",
            access_log=False,
        )
