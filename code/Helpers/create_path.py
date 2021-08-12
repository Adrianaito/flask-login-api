import os.path


def create_path(folder_name, file_name):

    folder_path = f"~/{folder_name}"
    data_folder = os.path.join(os.path.expanduser(folder_path), file_name)

    return data_folder
