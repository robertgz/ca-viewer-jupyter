from dataclasses import dataclass
from datetime import datetime
from typing import List

from . import download as sd_download

@dataclass
class XLSXFile():
    agency_shortcut: str
    year: str
    filename: str
    url: str

    def get_year(self):
        return self.year

    def get_filename(self):
        return self.filename

    def get_url(self):
        return self.url

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
        