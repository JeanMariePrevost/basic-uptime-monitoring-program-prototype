from typing import Optional


class URLTestResult:
    """
    Return object of a monitoring query which will contain all relevant information for a given query
    """

    def __init__(self, url: str, exists: bool, status_code: Optional[int], latency: Optional[float], error: Optional[str], timestamp: Optional[str] = None):
        self.url: str = url
        self.exists: bool = exists
        self.status_code: Optional[int] = status_code
        self.latency: Optional[float] = latency
        self.error: Optional[str] = error
        self.timestamp: Optional[str] = timestamp

    def __repr__(self) -> str:
        return f"URLTestResult(url={self.url}, exists={self.exists}, " f"status_code={self.status_code}, latency={self.latency}, " f"error={self.error})"

    def print_results(self) -> None:
        print("#################################")
        print(f'Results for "{self.url}":')
        print(f"URL exists: {self.exists}")
        print(f"Status code: {self.status_code}")
        print(f"Latency: {round(self.latency, 3)}s")

        if self.error is not None:
            print("Resulted in an error:")
            print(self.error)
            if "unknown url type" in self.error:
                print("(Hint: Are you missing a protocol? e.g. https://...)")
            if "Errno 11001" in self.error:
                print(f'(Hint: Could not resolve hostname "{self.url}")')
        print("#################################")
        print("")
