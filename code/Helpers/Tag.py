import uuid
from datetime import datetime
from japanera import Japanera
janera = Japanera()
import re


def createTag(id):
    '''
    Create tag with date/time and unique id
    '''
    dateTag = datetime.now().strftime("%y_%m_%d-%I_%M_%p_")
    # id = str(uuid.uuid4())
    fileName = dateTag + id
    return fileName


def only_digits(string: str, pattern="\D") -> str:

    only_digits = re.sub(
        pattern=pattern,
        repl="",
        string=string,
        count=0,
        flags=re.MULTILINE
    )

    return only_digits


def parse_heisei(date_string: str, pattern='%-E%-O年%m月%d日') -> str:
    parsed = janera.strptime(date_string, pattern)
    date_only = str(parsed[0].date())
    date_with_no_dash = only_digits(date_only)

    return date_with_no_dash


def parse_date(date_string: str) -> str:
    parsed_date = only_digits(date_string)
    count = len(parsed_date)
    if count < 6:
        parsed_date = parse_heisei(date_string)
    return parsed_date


def create_file_name(
        serial_number: int,
        date_of_receipt: int,
        date_string: str,
        sender: str) -> str:

    file_name = f"{serial_number} {date_of_receipt} {date_string} {sender}"

    return file_name
