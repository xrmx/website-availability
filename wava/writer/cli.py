import argparse
import logging
import sys

import dsnparse

from wava.writer.main import loop
from wava.args import parse_common_kafka_args
from wava.writer.postgres_writer import setup, write, cleanup
from wava.writer.exceptions import WriterConnectionError


logger = logging.getLogger()


def build_argument_parser():
    parser = argparse.ArgumentParser(description="Website availability checker writer")
    parse_common_kafka_args(parser)
    parser.add_argument(
        "--kafka-group-id",
        default="test-group",
        help="Kafka consumer group id, default: test-group",
    )
    parser.add_argument(
        "--kafka-poll-timeout",
        type=int,
        default=1000,
        help="Kafka consumer poll timeout in ms, default: 1000",
    )
    parser.add_argument(
        "--database-url",
        help="Database string connections, e.g. postgresql://user:password@host:port/dbname",
        default="postgresql://postgres:password@127.0.0.1:5432/test",
    )
    # FIXME: verbosity should handle default logger value
    parser.add_argument("--verbose", "-v", action="count", default=0)

    return parser


def main(*args):
    parser = build_argument_parser()
    args = parser.parse_args(*args)

    try:
        db = dsnparse.parse(args.database_url)
        if not db.paths:
            raise ValueError("missing database name")
    except ValueError as e:
        logger.error("Error in parsing database string: {}".format(str(e)))
        return sys.exit(1)

    config = {
        "kafka_brokers": args.kafka_broker,
        "kafka_topic": args.kafka_topic,
        "kafka_ssl_cafile": args.kafka_ssl_cafile,
        "kafka_ssl_certfile": args.kafka_ssl_certfile,
        "kafka_ssl_keyfile": args.kafka_ssl_keyfile,
        "kafka_poll_timeout": args.kafka_poll_timeout,
        "kafka_group_id": args.kafka_group_id,
        "db": {
            "user": db.username,
            "password": db.password,
            "host": db.host,
            "port": db.port,
            "dbname": db.paths[0],
        },
        "verbosity": args.verbose,
    }
    try:
        setup(config)
    except WriterConnectionError as e:
        logger.error("Connection error: {}".format(str(e.writer_original_exception)))
        return sys.exit(1)
    loop(config, write, cleanup)
