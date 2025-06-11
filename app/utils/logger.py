import logging
from pythonjsonlogger import jsonlogger
from pathlib import Path

class Logger:
    _instance = None

    def __new__(cls, name="realestate", log_to_file=True):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(name, log_to_file)
        return cls._instance

    def _initialize(self, name, log_to_file):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            formatter = jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            # Console (JSON)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # File (JSON)
            if log_to_file:
                Path("logs").mkdir(exist_ok=True)
                file_handler = logging.FileHandler("logs/resapp.json")
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger
