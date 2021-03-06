import psycopg2

from wava.writer.exceptions import (
    WriterConnectionError,
    WriterError,
)


def setup(config):
    """Setup the database tables"""

    sql = """CREATE TABLE IF NOT EXISTS wava_url (
        id BIGSERIAL PRIMARY KEY,
        url TEXT NOT NULL UNIQUE
    );
    CREATE TABLE IF NOT EXISTS wava_check (
        id BIGSERIAL PRIMARY KEY,
        url_id BIGSERIAL REFERENCES wava_url,
        ts timestamptz NOT NULL,
        http_response_time SMALLINT NOT NULL,
        http_status_code SMALLINT NOT NULL,
        content_matched BOOL NULL
    );"""

    # as seen on https://www.psycopg.org/docs/usage.html
    cur, conn = None, None
    try:
        conn = psycopg2.connect(**config["db"])
    except psycopg2.Error as e:
        raise WriterConnectionError(original_exception=e)

    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        try:
            if cur:
                cur.close()
            if conn:
                conn.close()
        except psycopg2.Error:
            pass
        raise WriterError(original_exception=e)


def write(config, payload):
    """Writes the payload into the database tables"""
    insert_url_sql = "INSERT INTO wava_url (url) VALUES (%s) ON CONFLICT DO NOTHING;"
    insert_url_params = (payload["url"],)

    get_url_id_sql = "SELECT id FROM wava_url WHERE url = %s"
    get_url_id_params = (payload["url"],)

    insert_check_sql = (
        "INSERT INTO wava_check (url_id, ts, http_response_time, http_status_code, content_matched) "
        "VALUES (%s, %s, %s, %s, %s);"
    )

    # TODO: reuse the connection
    conn, cur = None, None
    try:
        conn = psycopg2.connect(**config["db"])
        cur = conn.cursor()
        cur.execute(insert_url_sql, insert_url_params)
        cur.execute(get_url_id_sql, get_url_id_params)
        (url_id,) = cur.fetchone()
        insert_check_params = (
            url_id,
            payload["ts"],
            payload["http_response_time"],
            payload["status_code"],
            payload["content_matched"],
        )
        cur.execute(insert_check_sql, insert_check_params)
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        try:
            if cur:
                cur.close()
            if conn:
                conn.close()
        except psycopg2.Error:
            pass
        raise WriterError(original_exception=e)


def cleanup(config, consumer):
    """Cleanup function called on exit"""
    consumer.close()
