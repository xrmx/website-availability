from unittest import mock

from wava.writer.cli import main
from wava.writer.postgres_writer import write, cleanup


def test_main_validates_dsn_without_schema():
    with mock.patch("wava.checker.cli.sys.exit") as exit_mock:
        main(["--database-url", "schema:less@127.0.0.1:5432/test"])
    exit_mock.assert_called_once_with(1)


def test_main_validates_dsn_without_dbname():
    with mock.patch("wava.checker.cli.sys.exit") as exit_mock:
        main(["--database-url", "postrgresql://user:password@127.0.0.1:5432/"])
    exit_mock.assert_called_once_with(1)


def test_main_calls_loop_properly():
    with mock.patch("wava.writer.cli.loop") as loop_mock:
        with mock.patch("wava.writer.cli.setup") as setup_mock:
            main(["--database-url", "postgresql://user:password@127.0.0.1:5433/dbname"])

    config = {
        "kafka_brokers": "kafka-wava-d538bd8-riccardo-ae5f.aivencloud.com:27652",
        "kafka_topic": "test",
        "kafka_ssl_cafile": "ca.pem",
        "kafka_ssl_certfile": "service.cert",
        "kafka_ssl_keyfile": "service.key",
        "kafka_poll_timeout": 1000,
        "kafka_group_id": "test-group",
        "db": {
            "user": "user",
            "password": "password",
            "host": "127.0.0.1",
            "port": 5433,
            "dbname": "dbname",
        },
        "verbosity": 0,
    }
    setup_mock.assert_called_once_with(config)
    loop_mock.assert_called_once_with(config, write, cleanup)
