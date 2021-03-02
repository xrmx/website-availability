from unittest import mock

from wava.checker.cli import main
from wava.checker.requests_checker import check, cleanup


def test_main_validates_url():
    with mock.patch("wava.checker.cli.sys.exit") as exit_mock:
        main(["--url", "http://127.0.0.1"])
    exit_mock.assert_called_once_with(1)


def test_main_validates_regular_expression():
    with mock.patch("wava.checker.cli.sys.exit") as exit_mock:
        main(["--url", "http://example.com", "--content-match", "["])
    exit_mock.assert_called_once_with(1)


def test_main_calls_loop_properly():
    with mock.patch("wava.checker.cli.loop") as loop_mock:
        main(["--url", "http://example.com"])
    loop_mock.assert_called_once_with({
        "url": "http://example.com",
        "kafka_brokers": "kafka-wava-d538bd8-riccardo-ae5f.aivencloud.com:27652",
        "kafka_topic": "test",
        "kafka_ssl_cafile": "ca.pem",
        "kafka_ssl_certfile": "service.cert",
        "kafka_ssl_keyfile": "service.key",
        "interval": 60,
        "timeout": 1,
        "content_re": None,
        "verbosity": 0,
    }, check, cleanup)
