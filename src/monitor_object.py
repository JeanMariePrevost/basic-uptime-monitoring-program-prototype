import datetime

from monitoring_functions import check_url_through_urllib


class MonitorObject:
    """
    A class to represent a single monitor, running periodic tests for a url
    """

    title: str
    url: str
    last_result_status: str | None
    last_result_timestamp: str | None
    next_test_timestamp: str  # The monitor will run its test if the current time is greater than this
    test_interval_in_seconds: int  # The interval to be added to the next_test_datetime after each test

    def __init__(self, title: str, url: str, test_interval_in_seconds: int, last_result: str | None = None, last_result_timestamp: str | None = None, next_test_timestamp: str | None = None):
        self.title = title
        self.url = url
        self.last_result = last_result
        self.last_result_timestamp = last_result_timestamp
        self.next_test_timestamp = next_test_timestamp
        self.test_interval_in_seconds = test_interval_in_seconds
        if self.next_test_timestamp is None:
            self.next_test_timestamp = datetime.datetime.now().isoformat()

    def __repr__(self):
        return f"MonitorObject(title={self.title}, url={self.url}, last_result={self.last_result}, last_result_timestamp={self.last_result_timestamp}, next_test_timestamp={self.next_test_timestamp}, test_interval_in_seconds={self.test_interval_in_seconds})"

    def execute_test_if_due(self) -> None:
        """
        Executes the test if the current time is greater than the next test timestamp
        """
        if datetime.datetime.now() >= datetime.datetime.fromisoformat(self.next_test_timestamp):
            print(f"Test was due for monitor {self.title}. Executing...")
            try:
                result = check_url_through_urllib(self.url)
                self.last_result = "up" if result.exists else "down"
            except Exception as e:
                print(f"Error while executing test for monitor {self.title}: {e}")
                self.last_result = "error encountered"
            finally:
                self.last_result_timestamp = datetime.datetime.now().isoformat()
                self.next_test_timestamp = (datetime.datetime.now() + datetime.timedelta(seconds=self.test_interval_in_seconds)).isoformat()
        else:
            print(f"Test was not due for monitor {self.title}. Skipping...")