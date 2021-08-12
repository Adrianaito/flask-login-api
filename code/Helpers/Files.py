import base64
from os import name
from .Tag import createTag
import csv
from base64 import b64decode


def csv_writer(data, path, header: str = 'company, invoice, day, month, year'):

    destination_path = path

    with open(destination_path, 'w') as f:

        writer = csv.writer(f)
        writer.writerow([header])
        for page in data:
            v = page.values()
            writer.writerow([v])


def save_pdf_local(b64_data, folder, extension, name):
    '''
    Decode base64 to pdf and save to local.
    Returns file name
    '''
    # folder = "tmp/"
    # extension = ".pdf"
    # data = base64

    file_path = f"{folder}/{name}.{extension}"

    # file = open(file_path, 'wb')
    with open(file_path, 'wb') as f:
        decodedFile = base64.b64decode(b64_data)
        f.write(decodedFile)
        f.close()

    return True
