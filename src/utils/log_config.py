import logging


class CustomFormatter(logging.Formatter):
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    RED = "\033[1;31m"
    RESET = "\033[0;0m"

    FORMATS = {
        logging.DEBUG: GREEN + "%(asctime)s - %(levelname)s - %(message)s" + RESET,
        logging.INFO: GREEN + "%(asctime)s - %(levelname)s - %(message)s" + RESET,
        logging.WARNING: YELLOW + "%(asctime)s - %(levelname)s - %(message)s" + RESET,
        logging.ERROR: RED + "%(asctime)s - %(levelname)s - %(message)s" + RESET,
        logging.CRITICAL: RED + "%(asctime)s - %(levelname)s - %(message)s" + RESET
    }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format)
        return formatter.format(record)


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

# checking for existing hadlers
# def setup_logger():
#     logger = logging.getLogger()
#     if not logger.hasHandlers():  # Check if the logger already has handlers
#         logger.setLevel(logging.INFO)
#
#         ch = logging.StreamHandler()
#         ch.setFormatter(CustomFormatter())
#         logger.addHandler(ch)

# removing existing handler before establishing new handler
# def setup_logger():
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)
#
#     # Remove all existing handlers
#     for handler in logger.handlers[:]:
#         logger.removeHandler(handler)
#
#     ch = logging.StreamHandler()
#     ch.setFormatter(CustomFormatter())
#     logger.addHandler(ch)
