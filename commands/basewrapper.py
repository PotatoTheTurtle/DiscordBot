from datetime import datetime


class Base(object):
    def info_logger(self, message):
        print(f"[{datetime.today()} - INFO] {message}")

    def error_logger(self, message):
        raise Exception(f"[{datetime.today()} - **ERROR**] {message}")

    def warning_logger(self, message):
        print(f"[{datetime.today()} - *WARNING*] {message}")
