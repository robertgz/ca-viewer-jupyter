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
    _filings: List[NetFileFiling] = field(default_factory=list[NetFileFiling])

    def get_name(self):
        return self.name

    def get_agency_shortcut(self):
        return self.shortcut
    
    def load_filings(self, force=False):
        if len(self._filings) < 1 or force:
            print(f'Loading filings for agency {self.name} ...')
            self._filings = NetFileFiling.get_filings(self.shortcut)       

    def load_years(self, force=False):
        self.load_filings(force)

    def get_years(self) -> List[str]:       
        years = [x.get_year() for x in self._filings]

        # Only keep valid years
        years = [x for x in years if x]

        # Remove duplicate years with set
        return sorted(list(set(years)), reverse=True)

    @staticmethod
    def get_agencies():
        agencies = net_file_agency_download()['agencies']
        net_file_agencies = [NetFileAgency(**agency) for agency in agencies]

        skip_list = ['SUPER', 'CA', 'COR_bak', 'SFO']
        filtered_agencies = [x for x in net_file_agencies if x.shortcut not in skip_list]
        
        return filtered_agencies
