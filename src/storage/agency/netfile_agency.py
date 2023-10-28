from dataclasses import dataclass, field
from typing import List

from .base_agency import BaseAgency
from src.netfile.agency.download import download_agencies as net_file_agency_download
from src.netfile.filing.netfile_filing import NetFileFiling

@dataclass(kw_only=True)
class NetFileAgency(BaseAgency):
    id: int
    shortcut: str
    name: str
    filings: List[NetFileFiling] = field(default_factory=list[NetFileFiling])

    def get_name(self):
        return self.name

    def get_agency_shortcut(self):
        return self.shortcut

    def get_years(self) -> List[str]:
        if (len(self.filings) < 1):
            print('filings empty')
            self.filings = NetFileFiling.get_filings(self.get_agency_shortcut())
        
        return sorted(list(set([x.get_year() for x in self.filings])), reverse=True)

    @staticmethod
    def get_agencies():
        agencies = net_file_agency_download()['agencies']
        net_file_agencies = [NetFileAgency(**agency) for agency in agencies]

        skip_list = ['SUPER', 'CA', 'COR_bak', 'SFO']
        filtered_agencies = [x for x in net_file_agencies if x.shortcut not in skip_list]
        
        return filtered_agencies
