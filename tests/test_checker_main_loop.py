import json
from datetime import datetime, timezone
from unittest import mock

from wava.checker.main import loop


def test_loop_catches_keyboard_interrupt():
    check_mock = mock.MagicMock(side_effect=KeyboardInterrupt)
    cleanup_mock = mock.MagicMock()
    producer_mock = mock.MagicMock()
    config = {
        "interval": 1,
        "kafka_brokers": "foo",
        "kafka_ssl_cafile": "ca",
        "kafka_ssl_certfile": "cert",
        "kafka_ssl_keyfile": "key",
    }
    with mock.patch("wava.checker.main.KafkaProducer") as kafka_mock:
        kafka_mock.return_value = producer_mock
        loop(config, check_mock, cleanup_mock)
    check_mock.assert_called_once_with(config)
    cleanup_mock.assert_called_once_with(config, producer_mock)


def test_loop_push_serialized_check_response_to_kafka():
    now = datetime.now(timezone.utc)
    check_response = {
        "ts": now.isoformat(),
        "url": "http://example.com",
        "http_response_time": 100,
        "status_code": 200,
        "content_matched": None,
    }
    encoded_payload = json.dumps(check_response).encode("utf-8")
    producer_mock = mock.MagicMock()
    check_mock = mock.MagicMock(return_value=check_response)
    cleanup_mock = mock.MagicMock()
    config = {
        "interval": 1,
        "kafka_topic": "topic",
        "kafka_brokers": "foo",
        "kafka_ssl_cafile": "ca",
        "kafka_ssl_certfile": "cert",
        "kafka_ssl_keyfile": "key",
        "verbosity": 0,
    }
    with mock.patch("wava.checker.main.KafkaProducer") as kafka_mock:
        kafka_mock.return_value = producer_mock
        with mock.patch("wava.checker.main.sleep") as sleep_mock:
            sleep_mock.side_effect = KeyboardInterrupt
            loop(config, check_mock, cleanup_mock)

    kafka_mock.assert_called_once_with(
        bootstrap_servers=config["kafka_brokers"],
        security_protocol="SSL",
        ssl_cafile=config["kafka_ssl_cafile"],
        ssl_certfile=config["kafka_ssl_certfile"],
        ssl_keyfile=config["kafka_ssl_keyfile"],
    )
    check_mock.assert_called_once()

    producer_mock.flush.assert_called_once()
    producer_mock.send.assert_called_once_with(config["kafka_topic"], encoded_payload)
    sleep_mock.assert_called_once_with(1)
