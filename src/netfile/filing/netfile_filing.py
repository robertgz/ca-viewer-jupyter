
from enum import Enum
from dataclasses import dataclass
import pandas as pd

from src.netfile.filing.download import get_all_agency_filings

class Form(Enum):
    FORM_450 = 29 # Recipient Committee Campaign Statement – Short Form
    FORM_460 = 30 # Recipient Committee Campaign Statement
    FORM_461 = 31 # Major Donor and Independent Expenditure Committee Campaign Statement
    FORM_465 = 32 # Supplemental Independent Expenditure Report
    FORM_496 = 36 # Independent Expenditure Report
    FORM_497LCM = 38 # Contribution Report
    FORM_497 = 39 # Contribution Report

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
            date_range = self.title.partition(' (')[2].strip(')').strip()
            if len(date_range) < 1: # no date found
                return None
            
            if '-' not in date_range: # parse year from one date
                return date_range.split('/')[2]
            
            if '-' in date_range: # split into multiple dates
                dates = date_range.partition('-')
                if dates[0]: # parse year from first date
                    return dates[0].split('/')[2].strip()
                elif dates[2]: # parse year from second date
                    return dates[2].split('/')[2].strip()
        
        except Exception as e:
            print(f'Title not able to be parsed for year: {self.title}, id: {self.id}')
            return None

    def export_filer(self):
        return {'id':self.filerLocalId, 'name': self.filerName}

    @staticmethod
    def get_filings(agency_shortcut: str, form=Form.FORM_460.value):
        filings = get_all_agency_filings(agency_shortcut, form) 
        unique_filings = pd.DataFrame(filings).drop_duplicates().to_dict('records')
        net_file_filings = [NetFileFiling(**filing) for filing in unique_filings]

        filtered_filings = [x for x in net_file_filings if x.isEfiled == True]

        return filtered_filings

    @staticmethod
    def download_filings_460(agency_shortcut: str):
        return NetFileFiling.get_filings(agency_shortcut, form=Form.FORM_460.value)

    @staticmethod
    def download_filings_496(agency_shortcut: str):
        return NetFileFiling.get_filings(agency_shortcut, form=Form.FORM_496.value)

    @staticmethod
    def download_filings_497(agency_shortcut: str):
        return NetFileFiling.get_filings(agency_shortcut, form=Form.FORM_497.value)
