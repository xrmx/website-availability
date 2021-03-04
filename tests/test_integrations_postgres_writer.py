from datetime import datetime, timezone

import psycopg2
import pytest

from wava.writer.postgres_writer import setup as pgsetup, write


@pytest.fixture
def config():
    return {
        "db": {
            "user": "postgres",
            "password": "password",
            "host": "127.0.0.1",
            "port": 5432,
            "dbname": "postgres",
        }
    }


@pytest.mark.postgres
def test_can_setup_database(config):
    pgsetup(config)


@pytest.mark.postgres
def test_can_call_setup_more_than_one_time(config):
    pgsetup(config)
    pgsetup(config)


@pytest.mark.postgres
def test_can_write_in_setupped_database(config):
    pgsetup(config)
    now = datetime.now(timezone.utc)
    payload = {
        "url": "http://example.com",
        "ts": now.isoformat(),
        "http_response_time": 100,
        "status_code": 200,
        "content_matched": None,
    }
    write(config, payload)
    write(config, payload)

    conn = psycopg2.connect(**config["db"])
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM wava_url;")
    (wava_url_count,) = cur.fetchone()
    assert wava_url_count == 1
    cur.execute("SELECT COUNT(*) FROM wava_check;")
    (wava_check_count,) = cur.fetchone()
    assert wava_check_count == 2

    cur.close()
    conn.close()
