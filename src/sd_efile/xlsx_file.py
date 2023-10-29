import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, ClassVar

import pandas as pd

from . import download as sd_download

@dataclass
class XLSXFile():
    agency_shortcut: str
    year: str
    filename: str
    url: str

    sub_directory: ClassVar[str] = 'downloads'

    def get_year(self):
        return self.year

    def get_filename(self):
        return self.filename

    def get_url(self):
        return self.url
    
    def get_workbook(self):
        filepath = os.path.join(XLSXFile.get_local_download_path(), self.filename)
        if not os.path.isfile(filepath):
            XLSXFile.download_file(filepath, self.url)

        return pd.ExcelFile(filepath) # need to wrap this in a Workbook class

    @staticmethod
    def init_years(agency_shortcut: str):
        year_limit = 2000
        year = int(datetime.today().strftime('%Y'))
        xlsx_files: List[XLSXFile] = []

        year_found = True
        while year_found and year > year_limit:
            json_response = sd_download.request_download_url(year)

            if 'success' in json_response:
                file_info = {
                    'agency_shortcut': agency_shortcut,
                    'year': str(year),
                    'filename': (json_response['data']).split('/')[-1],
                    'url': json_response['data'],
                }
                xlsx_files.append(XLSXFile(**file_info))
            else:
                year_found = False
            year -= 1

        return xlsx_files
        
    @staticmethod
    def get_local_download_path():
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, XLSXFile.sub_directory)
    
    @staticmethod
    def download_file(filepath: str, url: str):
        download_path = XLSXFile.get_local_download_path()
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        file_data = sd_download.download_file(url)
        with open(filepath, 'wb') as file:
            file.write(file_data)
    