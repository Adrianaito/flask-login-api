import logging


def get_custom_logger(logName, filename, logLevel=logging.DEBUG, logFormat="%(message)s"):
    shipLogFormatter = logging.Formatter(
        fmt=logFormat,
    )

    shipLogHandler = logging.FileHandler(
        filename="./logs/" + filename,
    )
    shipLogHandler.setFormatter(shipLogFormatter)

    logs = logging.getLogger(logName)
    logs.setLevel(logLevel)
    logs.addHandler(shipLogHandler)

    return logs
