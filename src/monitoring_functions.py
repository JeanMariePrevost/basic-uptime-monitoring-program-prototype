"""
monitoring_functions.py

This module contains the functions for all "tests" to be run on web resources
"""

import time
import urllib.error
import urllib.request
from typing import Optional

from my_logger import general_logger
from url_test_result import URLTestResult


def check_url_through_urllib(url: str) -> URLTestResult:
    """
    Basic test that checks the status of a URL and returns the result.
    """
    general_logger.debug(f'Running check_url_through_urllib for url "{url}"')
    start_time = time.time()
    timestamp: str = time.ctime()
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
        if "unknown url type" in str(e):
            error = "Invalid URL, missing protocol"
        else:
            error: Optional[str] = f"Value Error: {e}"
    except urllib.error.URLError as e:
        latency = time.time() - start_time
        error: Optional[str] = f"URL Error: {e}"
    finally:
        result = URLTestResult(url, exists, status_code, latency, error, timestamp)
        general_logger.debug(f"check_url_through_urllib result: {result}")
        return result
