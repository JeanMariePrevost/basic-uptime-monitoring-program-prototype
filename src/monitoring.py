"""
monitoring.py

This module contains the functions for all "tests" to be run on web resources
"""

import time
import urllib.error
import urllib.request
from typing import Optional

from url_test_result import URLTestResult


def check_url_through_urllib(url: str) -> URLTestResult:
    """
    Basic test that checks the status of a URL and returns the result.
    """
    print(f'Running a basic test on url "{url}"')
    start_time = time.time()
    latency: Optional[float] = None
    status_code: Optional[int] = None
    error: Optional[str] = None
    exists: bool = False

    try:
        with urllib.request.urlopen(url) as response:
            latency = time.time() - start_time
            exists = response.status == 200
            status_code = response.status
    except urllib.error.HTTPError as e:
        latency = time.time() - start_time
        error: Optional[str] = f"HTTP Error {e.code}"
    except ValueError as e:
        latency = time.time() - start_time
        error: Optional[str] = f"Value Error: {e}"
    except urllib.error.URLError as e:
        latency = time.time() - start_time
        error: Optional[str] = f"URL Error: {e}"

    return URLTestResult(url, exists, status_code, latency, error)
