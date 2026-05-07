from datetime import datetime


class Logger:

    @staticmethod
    def log(component: str, message: str):
        current_time = datetime.now().strftime("%H:%M:%S")

        print(f"[{current_time}] [{component}] {message}")