from dataclasses import dataclass
from typing import List

from .base_agency import BaseAgency

@dataclass(kw_only=True)
class EFileAgency(BaseAgency):
    agency_shortcut: str
    name: str

    def get_name(self):
        return self.name

    def get_agency_shortcut(self):
        return self.agency_shortcut

    # def get_years() -> List(str):
    # runs year requests to get years
    #     pass

    @staticmethod
    def get_agencies():
        CSD = EFileAgency(agency_shortcut = 'CSD_new', name = 'San Diego, City of (2014-)')
        return [CSD]
