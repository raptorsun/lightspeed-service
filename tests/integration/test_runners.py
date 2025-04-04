"""Integration tests for runners."""

import ssl
from unittest.mock import patch

import pytest

from ols import config
from ols.runners.quota_scheduler import start_quota_scheduler
from ols.runners.uvicorn import start_uvicorn

MINIMAL_CONFIG_FILE = "tests/config/valid_config.yaml"
CORRECT_CONFIG_FILE = "tests/config/config_for_integration_tests.yaml"
QUOTA_LIMITERS_CONFIG_FILE = (
    "tests/config/config_for_integration_tests_quota_limiters.yaml"
)


def test_start_uvicorn_minimal_setup():
    """Test the function to start Uvicorn server."""
    config.reload_from_yaml_file(MINIMAL_CONFIG_FILE)

    # don't start the real Uvicorn server
    with patch("uvicorn.run") as mocked_runner:
        start_uvicorn(config)
        mocked_runner.assert_called_once_with(
            "ols.app.main:app",
            host="0.0.0.0",  # noqa: S104
            port=8080,
            workers=1,
            log_level=30,
            ssl_keyfile=None,
            ssl_certfile=None,
            ssl_keyfile_password=None,
            ssl_version=ssl.PROTOCOL_TLS_SERVER,
            ssl_ciphers="TLSv1",
            access_log=False,
        )


def test_start_uvicorn_full_setup():
    """Test the function to start Uvicorn server."""
    config.reload_from_yaml_file(CORRECT_CONFIG_FILE)
    # don't start the real Uvicorn server
    with patch("uvicorn.run") as mocked_runner:
        start_uvicorn(config)
        mocked_runner.assert_called_once_with(
            "ols.app.main:app",
            host="0.0.0.0",  # noqa: S104
            port=8080,
            workers=1,
            log_level=30,
            ssl_keyfile="tests/config/key",
            ssl_certfile="tests/config/empty_cert.crt",
            ssl_keyfile_password="* this is password *",  # noqa: S106
            ssl_version=ssl.TLSVersion.TLSv1_3,
            ssl_ciphers="TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",  # noqa: E501
            access_log=False,
        )


@pytest.mark.filterwarnings("ignore")
def test_start_quota_scheduler():
    """Test the function to start Quota scheduler."""
    config.reload_from_yaml_file(QUOTA_LIMITERS_CONFIG_FILE)
    with (
        patch("ols.runners.quota_scheduler.sleep", side_effect=Exception()),
        patch("psycopg2.connect"),
    ):
        # just try to enter the endless loop
        start_quota_scheduler(config)
