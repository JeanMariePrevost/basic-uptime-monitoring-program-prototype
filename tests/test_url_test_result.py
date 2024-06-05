from src.url_test_result import URLTestResult


def test_initialization():
    url_test_result = URLTestResult(
        url="http://thisisatest.com",
        exists=True,
        status_code=200,
        latency=0.123,
        error=None,
    )
    assert url_test_result.url == "http://thisisatest.com"
    assert url_test_result.exists is True
    assert url_test_result.status_code == 200
    assert url_test_result.latency == 0.123
    assert url_test_result.error is None
