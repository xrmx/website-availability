from unittest import mock

import psycopg2
import pytest

from wava.writer.exceptions import (
    WriterConnectionError,
    WriterError,
)
from wava.writer.postgres_writer import setup as pgsetup, write, cleanup


def test_setup_raises_WriterConnectionError_if_connect_fails():
    with pytest.raises(WriterConnectionError):
        with mock.patch("wava.writer.postgres_writer.psycopg2.connect") as connect_mock:
            connect_mock.side_effect = psycopg2.InterfaceError
            config = {"db": {}}
            pgsetup(config)


def test_setup_raises_WriterError_if_query_fails():
    with pytest.raises(WriterError):
        with mock.patch("wava.writer.postgres_writer.psycopg2.connect") as connect_mock:
            cursor_mock = mock.MagicMock()
            cursor_mock.cursor.side_effect = psycopg2.InterfaceError
            connect_mock.return_value = cursor_mock
            config = {"db": {}}
            pgsetup(config)


def test_check_matcher_match_content_re_with_body():
    with pytest.raises(WriterError):
        with mock.patch("wava.writer.postgres_writer.psycopg2.connect") as connect_mock:
            connect_mock.side_effect = psycopg2.Error
            write({"db": {}}, {"url": "url"})


def test_cleanup_calls_consumer_close():
    consumer_mock = mock.MagicMock()
    cleanup({}, consumer_mock)
    consumer_mock.called_once()
