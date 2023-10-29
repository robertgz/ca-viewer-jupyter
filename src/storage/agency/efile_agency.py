from dataclasses import dataclass, field
from typing import List

import pandas as pd

from .base_agency import BaseAgency
from src.sd_efile.xlsx_file import XLSXFile
from src.storage.filer.efile_filer import EFileFiler

@dataclass(kw_only=True)
class EFileAgency(BaseAgency):
    agency_shortcut: str
    name: str
    xlsx_file_metadata: List[XLSXFile] = field(default_factory=list[XLSXFile])

    def get_name(self):
        return self.name

    def get_agency_shortcut(self):
        return self.agency_shortcut
    
    def populate_files(self):
        if (len(self.xlsx_file_metadata) < 1):
            print('files empty')
            self.xlsx_file_metadata = XLSXFile.init_years(self.agency_shortcut)

    def get_years(self) -> List[str]:
        self.populate_files()
        return [x.get_year() for x in self.xlsx_file_metadata]

    def _get_filers_for_year(self, year: str) -> pd.DataFrame:
        converter = EFileFiler.get_converter()
        file = next(i for i in self.xlsx_file_metadata if i.get_year() == year)
        return file.get_workbook().get_summary_data_frame(converter)

    def get_filers_by_year(self, year: str):
        self.populate_files()    
        filers_df = self._get_filers_for_year(year)
        return EFileFiler.get_filers(filers_df)

    def get_filers(self):
        self.populate_files()
        filers_dfs = [self._get_filers_for_year(year) for year in self.get_years()]
        filers = pd.concat(filers_dfs)
        return EFileFiler.get_filers(filers)

    @staticmethod
    def get_agencies():
        CSD = EFileAgency(agency_shortcut = 'CSD_new', name = 'San Diego, City of (2014-)')
        return [CSD]
