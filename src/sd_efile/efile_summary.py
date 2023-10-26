import math
from dataclasses import dataclass

@dataclass
class EFileSummary():
    Filer_ID: int
    Filer_NamL: str
    Report_Num: str
    e_filing_id: str
    orig_e_filing_id: str
    Cmtte_Type: str
    Rpt_Date: int
    From_Date: int
    Thru_Date: int
    Elect_Date: str
    Rec_Type: str
    Form_Type: str
    Line_Item: int
    Amount_A: float
    Amount_B: float
    Amount_C: float

    def _get_year(self):
        summary = self
        year = None
        if len(str(summary.From_Date)) > 3:
            year = str(summary.From_Date)[:4]
        elif len(str(summary.Thru_Date)) > 3:
            year = str(summary.Thru_Date)[:4]
        return year

    def to_common(self, agency_shortcut: str):
        common_summary = {
            "agency_shortcut": agency_shortcut,            
            "year": self._get_year(),
            # Added fields above

            'filer_local_id': None,
            'filer_id': str(self.Filer_ID),
            'filer_name': self.Filer_NamL,
            'filing_id': str(self.e_filing_id),
            # 'filing_date': ,
            "form_type": self.Form_Type,
            "line_item": str(self.Line_Item),
            "amount_a": float(0) if math.isnan(self.Amount_A) else self.Amount_A,
            "amount_b": float(0) if math.isnan(self.Amount_B) else self.Amount_B,
            "amount_c": float(0) if math.isnan(self.Amount_C) else self.Amount_C,
        }
        return common_summary
