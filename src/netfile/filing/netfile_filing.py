
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
            return self.title.partition(' (')[2].partition('-')[0].strip().split('/')[2]
        except Exception as e:
            try:
                return self.title.partition(' (')[2].partition('-')[2].strip().split('/')[2].strip(')')
            except Exception as e:
                print(f'Title not able to be parsed for year: {self.title}, id: {self.id}')
                return None

    @staticmethod
    def get_filings(agency_shortcut: str, form=Form.FORM_460.value):
        filings = get_all_agency_filings(agency_shortcut, form) 
        unique_filings = pd.DataFrame(filings).drop_duplicates().to_dict('records')
        net_file_filings = [NetFileFiling(**filing) for filing in unique_filings]

        filtered_filings = [x for x in net_file_filings if x.isEfiled == True]

        return filtered_filings
