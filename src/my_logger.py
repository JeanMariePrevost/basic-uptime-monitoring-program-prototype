import logging
import os

from colorlog import ColoredFormatter

# Step 1: Create loggers
general_logger = logging.getLogger("general")  # App-wide events logging, excluding monitor results
monitor_logger = logging.getLogger("monitor_results")  # Monitor results logging only

# Step 2: Set log levels
general_logger.setLevel(logging.INFO)
monitor_logger.setLevel(logging.INFO)

# Step 3: Create formatters
general_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
monitor_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]")

# Create a colored formatter for console output, much better than everything being red
color_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
    secondary_log_colors={},
    style="%",
)

# Step 4: Create handlers
console_handler = logging.StreamHandler()  # Output to console
if not os.path.exists("logs"):  # Create logs directory if it doesn't exist
    os.makedirs("logs")
file_handler_general = logging.FileHandler("logs/app_events.log")
file_handler_monitor = logging.FileHandler("logs/monitor_results.log")

# Step 5: Attach formatters to handlers
console_handler.setFormatter(color_formatter)
file_handler_general.setFormatter(general_formatter)
file_handler_monitor.setFormatter(monitor_formatter)

# Step 6: Attach handlers to loggers
general_logger.addHandler(console_handler)
general_logger.addHandler(file_handler_general)

monitor_logger.addHandler(console_handler)
monitor_logger.addHandler(file_handler_monitor)


# Quick levels guide
# general_logger.debug("This is a debug message")
# general_logger.info("This is an info message")
# general_logger.warning("This is a warning message")
# general_logger.error("This is an error message")
# general_logger.critical("This is a critical message")
