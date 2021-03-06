from datetime import datetime, timezone

import requests
from requests.exceptions import RequestException

from wava.checker.exceptions import CheckerNetworkError

SECONDS_TO_MS = 1000


def check(config):
    """The requests based implementation of the checker"""
    url = config["url"]
    timeout = config["timeout"]
    content_re = config["content_re"]

    try:
        response = requests.get(url, timeout=timeout)
    except RequestException as e:
        raise CheckerNetworkError(original_exception=e)

    if content_re:
        try:
            content_matched = bool(content_re.search(response.text))
        except TypeError:
            content_matched = False
    else:
        content_matched = None

    response_time_ms = int(response.elapsed.total_seconds() * SECONDS_TO_MS)
    now = datetime.now(timezone.utc)
    return {
        "ts": now.isoformat(),
        "url": url,
        "http_response_time": response_time_ms,
        "status_code": response.status_code,
        "content_matched": content_matched,
    }


def cleanup(config, producer):
    """Cleanup function called on exit"""
    producer.flush()
    producer.close()
