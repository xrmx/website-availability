import re
from unittest import mock

import pytest
import requests_mock
from requests.exceptions import RequestException

from wava.checker.exceptions import CheckerNetworkError
from wava.checker.requests_checker import check


def test_check_raises_proper_exception_on_requests_error():
    with requests_mock.Mocker() as m:
        m.get("http://example.com", exc=RequestException)
        with pytest.raises(CheckerNetworkError):
            check({
                "url": "http://example.com",
                "timeout": 1,
                "content_re": None,
            })


def test_check_returns_dictionary():
    with requests_mock.Mocker() as m:
        r = m.get("http://example.com", text="")
        response = check({
            "url": "http://example.com",
            "timeout": 1,
            "content_re": None,
        })
    assert response == {
        "http_response_time": mock.ANY,
        "status_code": 200,
        "content_matched": None,
    }


def test_check_matcher_match_content_re_with_body():
    with requests_mock.Mocker() as m:
        m.get("http://example.com", text="body")
        response = check({
            "url": "http://example.com",
            "timeout": 1,
            "content_re": re.compile(r"bo"),
        })
    assert response == {
        "http_response_time": mock.ANY,
        "status_code": 200,
        "content_matched": True,
    }
