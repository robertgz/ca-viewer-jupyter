import os
import datetime
from typing import List

import pandas as pd

from .xlsx_file import XLSXFile
from . import download as sd_download
from . import file_storage as sd_file_storage

class Files:
    def __init__(self):
        self.xlsx_files: List[XLSXFile] = []

    def get_list(self):
        return self.file_item_list

    def init_years(self, agency_shortcut = 'CSD_EFILE'):
        year_limit = 2000

        if (len(self.xlsx_files) > 1):
            print('shared_lists NOT empty')
            return self.xlsx_files

        current_year = datetime.datetime.today().strftime('%Y')
        year = int(current_year)

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
                self.xlsx_files.append(XLSXFile(**file_info))
            else:
                year_found = False
            year -= 1

        return self.xlsx_files

    def get_years(self):
        return [x.get_year() for x in self.xlsx_files]

    def get_file_item(self, year: str):
        if len(self.xlsx_files) < 1:
            print('run init_years() first')
            raise UserWarning('Exit Early')
            return

        return next(x for x in self.xlsx_files if x.get_year() == year)

    def get_file_path(self, year: str):
        file_item = self.get_file_item(year)
        local_path = sd_file_storage.get_local_download_path()

        filepath = os.path.join(local_path, file_item.get_filename())

        sd_file_storage.conditionally_download(filepath, file_item.get_url())
        return filepath

    # Workbook
    summary_sheet_name = 'F460-Summary'

    def _get_year_workbook(self, year):
        filepath = self.get_file_path(year)

        return pd.ExcelFile(filepath)

    def get_sheet_names(self, year: str):
        workbook = self._get_year_workbook(year)
        return workbook.sheet_names

    def get_summary_worksheet(self, year):
        workbook = self._get_year_workbook(year)
        worksheet = workbook.parse(self.summary_sheet_name)
        return worksheet
    
    # Summaries
    def get_year_summaries(self, year: str):
        worksheet = self.get_summary_worksheet(year)
        summaries = worksheet.to_dict('records')
        return summaries
    
    @staticmethod
    def summaries_to_common(agency_shortcut: str, summaries):
        common_summaries = []
        for summary in summaries:
            common_summaries.append(
                {
                    'agency_shortcut': agency_shortcut,
                    'filer_local_id': None,
                    'filer_id': summary['Filer_ID'],
                    'filer_name': summary['Filer_NamL'],
                    'filing_id': summary['e_filing_id'],
                    "form_type": summary['Form_Type'],
                    "line_item": summary['Line_Item'],
                    "amount_a": summary['Amount_A'],
                    "amount_b": summary['Amount_B'],
                    "amount_c": summary['Amount_C'],
                }
            )
        return common_summaries

    def get_summaries(self, agency_shortcut: str, year: str):
        summaries = self.get_year_summaries(year)
        common_summaries = self.summaries_to_common(agency_shortcut, summaries)
        return common_summaries
    