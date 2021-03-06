import argparse
import logging
import re
import sys

import validators

from wava.args import parse_common_kafka_args
from wava.checker.main import loop
from wava.checker.requests_checker import check, cleanup


logger = logging.getLogger()


def build_argument_parser():
    parser = argparse.ArgumentParser(description="Website availability checker")
    parse_common_kafka_args(parser)
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Interval of the check in seconds, default: 60",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1,
        help="Timeout for request checker to wait for the first byte in seconds, default: 1",
    )
    parser.add_argument(
        "--content-match",
        help="Optional regular expression to search in the response body",
    )
    parser.add_argument("--url", required=True, help="The HTTP url to check")
    parser.add_argument("--verbose", "-v", action="count", default=0)

    return parser


def main(*args):
    parser = build_argument_parser()
    args = parser.parse_args(*args)

    valid_url = args.url.startswith("http") and validators.url(args.url, public=True)
    if not valid_url:
        logger.error("URL is invalid, only HTTP/HTTPS url are supported")
        return sys.exit(1)

    if args.content_match is not None:
        try:
            # FIXME: expect issues there as string is not raw :|
            content_re = re.compile(args.content_match)
        except re.error as e:
            logger.error("Invalid --content-match value: {}".format(str(e)))
            return sys.exit(1)
    else:
        content_re = None

    config = {
        "url": args.url,
        "kafka_brokers": args.kafka_broker,
        "kafka_topic": args.kafka_topic,
        "kafka_ssl_cafile": args.kafka_ssl_cafile,
        "kafka_ssl_certfile": args.kafka_ssl_certfile,
        "kafka_ssl_keyfile": args.kafka_ssl_keyfile,
        "interval": args.interval,
        "timeout": args.timeout,
        "content_re": content_re,
        "verbosity": args.verbose,
    }
    loop(config, check, cleanup)
