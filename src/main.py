import monitoring
import system_tray

if __name__ == "__main__":
    result1 = monitoring.check_url_through_urllib("http://google.com")
    result2 = monitoring.check_url_through_urllib("google.com")
    result3 = monitoring.check_url_through_urllib("http://thisurldoesnotexist.whatever")

    result1.print_results()
    result2.print_results()
    result3.print_results()
    system_tray.initialize_system_tray()
