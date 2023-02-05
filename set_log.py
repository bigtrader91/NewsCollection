import logging
def set_log():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create the file handler
    file_handler = logging.FileHandler("뉴스알리미.log")
    file_handler.setLevel(logging.DEBUG)

    # Create the formatter and add it to the file handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    return logger
