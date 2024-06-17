import datetime

from my_logger import general_logger, monitor_logger
from monitoring_functions import check_url_through_urllib


class MonitorObject:
    """
    Represents a monitor object that will be used to check the status of a URL.

    Is also the class that will be used to store the monitor objects in the monitors_list and serialized into json.
    """

    title: str
    url: str
    last_result_status: str | None
    last_result_error: str | None
    last_result_timestamp: str | None
    next_test_timestamp: str  # The monitor will run its test if the current time is greater than this
    test_interval_in_seconds: int  # The interval to be added to the next_test_datetime after each test

    def __init__(
        self,
        title: str,
        url: str,
        test_interval_in_seconds: int,
        last_result_status: str | None = None,
        last_result_error: str | None = None,
        last_result_timestamp: str | None = None,
        next_test_timestamp: str | None = None,
    ):
        self.title = title
        self.url = url
        self.last_result_status = last_result_status
        self.last_result_timestamp = last_result_timestamp
        self.next_test_timestamp = next_test_timestamp
        self.test_interval_in_seconds = test_interval_in_seconds
        if self.next_test_timestamp is None:
            self.next_test_timestamp = datetime.datetime.now().isoformat()
        general_logger.info(f"MonitorObject created with title={title}, url={url}, test_interval_in_seconds={test_interval_in_seconds}")

    def __repr__(self):
        return f"MonitorObject(title={self.title}, url={self.url}, last_result_status={self.last_result_status}, last_result_timestamp={self.last_result_timestamp}, next_test_timestamp={self.next_test_timestamp}, test_interval_in_seconds={self.test_interval_in_seconds})"

    def execute_test_if_due(self) -> bool:
        """
        Executes the test IF the current time is greater than the next test timestamp
        :return: True if the test was executed, False if it was skipped
        """
        test_was_executed = False
        if datetime.datetime.now() >= datetime.datetime.fromisoformat(self.next_test_timestamp):
            self.execute_test()
            test_was_executed = True
        else:
            # print(f"Test was not due for monitor {self.title}. Skipping...")
            pass

        return test_was_executed

    def execute_test(self) -> None:
        """
        Executes the test for the monitor
        """
        general_logger.debug(f"Executing test for monitor [{self.title}] with url={self.url}")
        result = check_url_through_urllib(self.url)
        general_logger.debug(f"Test result for monitor [{self.title}]: {result}")
        if result.error is not None:
            general_logger.debug(f"Monitor [{self.title}] test failed with error: {result.error}")
            monitor_logger.warning(f"Monitor [{self.title}] test failed with error: {result.error}")
        elif self.last_result_status == "up" and not result.exists:
            general_logger.debug(f"Monitor [{self.title}] has changed status from up to down")
            monitor_logger.warning(f"Monitor [{self.title}] has changed status from up to down. Error: {result.error}")
        elif self.last_result_status == "down" and result.exists:
            general_logger.info(f"Monitor [{self.title}] has changed status from down to up")
            monitor_logger.warning(f"Monitor [{self.title}] has changed status from down to up. Error: {result.error}")
        self.last_result_status = "up" if result.exists else "down"
        self.last_result_error = result.error
        self.last_result_timestamp = datetime.datetime.now().isoformat()
        self.next_test_timestamp = (datetime.datetime.now() + datetime.timedelta(seconds=int(self.test_interval_in_seconds))).isoformat()
