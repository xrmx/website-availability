import argparse
import logging
import re
import sys

import validators

from wava.checker.main import loop
from wava.checker.requests_checker import check, cleanup


logger = logging.getLogger()


def main():
    parser = argparse.ArgumentParser(description="Website availability checker")
    parser.add_argument("--interval", type=int, default=60, help="Interval of the check in seconds, default 60")
    parser.add_argument("--timeout", type=int, default=1, help="Timeout for request checker to wait for the first byte in seconds, default 1")
    parser.add_argument("--content-match", help="Regular expression to search in the response body")
    parser.add_argument("--url", required=True, help="The HTTP url to check")
    parser.add_argument('--verbose', '-v', action='count', default=0)

    args = parser.parse_args()

    valid_url = args.url.startswith("http") and validators.url(args.url, public=True)
    if not valid_url:
        logger.error("URL is invalid, only HTTP/HTTPS url are supported")
        sys.exit(1)

    if args.content_match is not None:
        try:
            # FIXME: expect issues there as string is not raw :|
            content_re = re.compile(args.content_match)
        except re.error as e:
            logger.error("Invalid --content-match value: {}".format(str))
            sys.exit(1)
    else:
        content_re = None

    config = {
        "url": args.url,
        "interval": args.interval,
        "timeout": args.timeout,
        "content_re": content_re,
        "verbosity": args.verbose,
    }
    loop(config, check, cleanup)
