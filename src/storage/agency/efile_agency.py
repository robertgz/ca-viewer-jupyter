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

    def _get_filers_for_year(self, year: str):
        file = next(i for i in self.xlsx_file_metadata if i.get_year() == year)
        return file.get_workbook().get_filers()

    def get_filers_by_year(self, year: str):
        self.populate_files()    
        filers = self._get_filers_for_year(year)
        return [EFileFiler(**filer) for filer in filers]

    def get_filers(self):
        self.populate_files()

        filers = []
        [filers.extend(self._get_filers_for_year(year)) for year in self.get_years()]
        filers = pd.DataFrame(filers).drop_duplicates().to_dict('records')

        return [EFileFiler(**filer) for filer in filers]

    @staticmethod
    def get_agencies():
        CSD = EFileAgency(agency_shortcut = 'CSD_new', name = 'San Diego, City of (2014-)')
        return [CSD]
