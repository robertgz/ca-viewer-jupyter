import os
from . import download as sd_download

def get_local_download_path():
    dirname = os.path.dirname(__file__)
    sub_directory = 'downloads'
    path = os.path.join(dirname, sub_directory)
    return path

def download_xlsx_to_disk(filepath: str, url: str):
    file_data = sd_download.download_file(url)
    with open(filepath, 'wb') as file:
        file.write(file_data)
    return filepath  

def conditionally_download(filepath, url):
    if not os.path.isfile(filepath):
        download_path = get_local_download_path()
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        download_xlsx_to_disk(filepath, url)
