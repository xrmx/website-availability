import requests
from requests.exceptions import RequestException

from wava.checker.exceptions import CheckerNetworkError


def check(config):
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

    return {
        "http_response_time": response.elapsed,
        "status_code": response.status_code,
        "content_matched": content_matched,
    }


def cleanup(config):
    pass