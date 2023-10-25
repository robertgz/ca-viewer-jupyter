from dataclasses import dataclass

@dataclass
class NetFileSummary():
    netFileKey: str
    externalId: str
    filerLocalId: str
    filerStateId: str
    filerName: str
    filingId: str
    filingStartDate: str
    filingEndDate: str
    rec_Type: str
    form_Type: str
    line_Item: str
    amount_A: float
    amount_B: float
    amount_C: float
    elec_Date: str

    @staticmethod
    def _get_year_from_summary(summary):
        year = None
        if len(summary.filingStartDate) > 0:
            year = summary.filingStartDate.partition('-')[0]
        elif len(summary.filingEndDate) > 0:
            year = summary.filingEndDate.partition('-')[0]
        return year

    def to_common(self, agency_shortcut: str):
        common_summary = {
            "agency_shortcut": agency_shortcut,            
            "year": self._get_year_from_summary(self),
            # Added fields above

            'filer_local_id': self.filerLocalId,
            'filer_id': self.filerStateId,
            'filer_name': self.filerName,
            'filing_id': self.filingId,
            "form_type": self.form_Type,
            "line_item": self.line_Item,
            "amount_a": self.amount_A,
            "amount_b": self.amount_B,
            "amount_c": self.amount_C,
        }
        return common_summary
