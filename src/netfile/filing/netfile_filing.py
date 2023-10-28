
from dataclasses import dataclass
import pandas as pd

from src.netfile.filing.download import get_all_agency_filings

@dataclass(kw_only=True)
class NetFileFiling():
    id: str
    agency: int
    isEfiled: bool
    hasImage: bool
    filingDate: str
    title: str
    form: int
    filerName: str
    filerLocalId: str
    filerStateId: str
    amendmentSequenceNumber: int
    amendedFilingId: str

    def get_year(self):
        try:
            return self.title.partition(' (')[2].partition('-')[0].strip().split('/')[2]
        except Exception as e:
            print(f'Title not able to be parsed: {self.title}, id: {self.id}')
            return None

    @staticmethod
    def get_filings(agency_shortcut: str):
        filings = get_all_agency_filings(agency_shortcut) 
        unique_filings = pd.DataFrame(filings).drop_duplicates().to_dict('records')
        net_file_filings = [NetFileFiling(**filing) for filing in unique_filings]

        filtered_filings = [x for x in net_file_filings if x.isEfiled == True]

        return filtered_filings
