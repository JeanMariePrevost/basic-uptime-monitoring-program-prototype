import urllib.request
import urllib.error
import time


def check_url_through_urllib(url: str) -> None:
    print("#################################")
    print(f'Running a basic test on url "{url}"')
    start_time = time.time()

    try:
        with urllib.request.urlopen(url) as response:
            latency = time.time() - start_time
            print(f'Results for "{url}":')
            print(f"URL exists: {response.status == 200}")
            print(f"Status code: {response.status}")
            print(f"Latency: {round(latency, 3)}s")
    except urllib.error.HTTPError as e:
        print(f"URL does not exist: HTTP Error {e.code}")
    except ValueError as e:
        print(f"Error: {e}")
        if "unknown url type" in str(e):
            print("(Are you missing a protocol? e.g. https://...)")
    except urllib.error.URLError as e:
        if "Errno 11001" in str(e):
            print(f'Could not resolve hostname "{url}"')
        else:
            print(f"Error: {e.reason}")
    finally:
        print("#################################")
        print("")


if __name__ == "__main__":
    check_url_through_urllib("http://google.com")
    check_url_through_urllib("google.com")
    check_url_through_urllib("http://thisurldoesnotexist.whatever")
