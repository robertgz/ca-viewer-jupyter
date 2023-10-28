from dataclasses import dataclass, field
from typing import List

from .base_agency import BaseAgency
from src.sd_efile.xlsx_file import XLSXFile

@dataclass(kw_only=True)
class EFileAgency(BaseAgency):
    agency_shortcut: str
    name: str
    xlsx_file_metadata: List[XLSXFile] = field(default_factory=list[XLSXFile])

    def get_name(self):
        return self.name

    def get_agency_shortcut(self):
        return self.agency_shortcut

    def get_years(self) -> List[str]:
        if (len(self.xlsx_file_metadata) < 1):
            self.xlsx_file_metadata = XLSXFile.init_years(self.agency_shortcut)

        return [x.get_year() for x in self.xlsx_file_metadata]

    @staticmethod
    def get_agencies():
        CSD = EFileAgency(agency_shortcut = 'CSD_new', name = 'San Diego, City of (2014-)')
        return [CSD]
