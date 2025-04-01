import logging


# ================
logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# ================
file_handler = logging.FileHandler(filename='src/logs/warning.log', mode="a")
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

# ================
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# ================
logger.addHandler(file_handler)
logger.addHandler(console_handler)
