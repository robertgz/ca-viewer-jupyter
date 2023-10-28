from dataclasses import dataclass
from typing import List

from .base_agency import BaseAgency
from src.netfile.agency.download import download_agencies as net_file_agency_download

@dataclass(kw_only=True)
class NetFileAgency(BaseAgency):
    id: int
    shortcut: str
    name: str

    def get_name(self):
        return self.name

    def get_agency_shortcut(self):
        return self.shortcut

    # def get_years() -> List[str]:
    # loads and saves agencies into class to get years
    #     pass

    @staticmethod
    def get_agencies():
        agencies = net_file_agency_download()['agencies']
        net_file_agencies = [NetFileAgency(**agency) for agency in agencies]

        skip_list = ['SUPER', 'CA', 'COR_bak', 'SFO']
        filtered_agencies = [x for x in net_file_agencies if x.shortcut not in skip_list]
        
        return filtered_agencies
