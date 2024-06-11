from src.monitoring_functions import check_url_through_urllib


def test_check_url_success():
    result = check_url_through_urllib("https://www.google.com")
    assert result.exists is True, "Should be able to succeed with https://www.google.com."


def test_check_url_without_protocol_failure():
    result = check_url_through_urllib("google.com")
    assert result.exists is False, "The URL without protocol should not be accessible."
    assert result.error is not None, "There should be an error for a URL without protocol."


def test_check_malformed_url_failure():
    result = check_url_through_urllib("this_url_does_not_exist")
    assert result.exists is False, "A non-existent domain should not be accessible."
    assert result.error is not None, "There should be an error for a non-existent domain."
