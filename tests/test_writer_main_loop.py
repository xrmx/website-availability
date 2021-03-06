import json
from unittest import mock

from wava.writer.main import loop


def test_loop_catches_keyboard_interrupt():
    write_mock = mock.MagicMock()
    cleanup_mock = mock.MagicMock()
    config = {
        "kafka_brokers": "foo",
        "kafka_topic": "topic",
        "kafka_group_id": "test-group",
        "kafka_poll_timeout": 1000,
        "kafka_ssl_cafile": "ca",
        "kafka_ssl_certfile": "cert",
        "kafka_ssl_keyfile": "key",
    }
    consumer_mock = mock.MagicMock()
    consumer_mock.poll.side_effect = KeyboardInterrupt

    with mock.patch("wava.writer.main.KafkaConsumer", return_value=consumer_mock):
        loop(config, write_mock, cleanup_mock)
    write_mock.assert_not_called()
    cleanup_mock.assert_called_once_with(config, consumer_mock)


def test_loop_send_decoded_payload_to_write():
    record_mock = mock.MagicMock()
    encoded_payload = json.dumps({"a": "payload"}).encode("utf-8")
    record_mock.value = encoded_payload
    consumer_mock = mock.MagicMock()
    consumer_mock.poll.return_value = {"topic": [record_mock]}
    consumer_mock.commit.side_effect = KeyboardInterrupt

    write_mock = mock.MagicMock()
    cleanup_mock = mock.MagicMock()
    config = {
        "kafka_topic": "topic",
        "kafka_brokers": "foo",
        "kafka_group_id": "test-group",
        "kafka_poll_timeout": 1000,
        "kafka_ssl_cafile": "ca",
        "kafka_ssl_certfile": "cert",
        "kafka_ssl_keyfile": "key",
    }

    with mock.patch(
        "wava.writer.main.KafkaConsumer", return_value=consumer_mock
    ) as kafka_mock:
        loop(config, write_mock, cleanup_mock)

    kafka_mock.assert_called_once_with(
        config["kafka_topic"],
        bootstrap_servers=config["kafka_brokers"],
        security_protocol="SSL",
        group_id=config["kafka_group_id"],
        ssl_cafile=config["kafka_ssl_cafile"],
        ssl_certfile=config["kafka_ssl_certfile"],
        ssl_keyfile=config["kafka_ssl_keyfile"],
    )
    write_mock.assert_called_once_with(config, {"a": "payload"})

    consumer_mock.commit.assert_called_once()
