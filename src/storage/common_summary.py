from dataclasses import dataclass

@dataclass
class CommonSummary():
    agency_shortcut: str
    year: str
    filer_local_id: str
    filer_id: str
    filer_name: str
    filing_id: str
    form_type: str
    line_item: str
    amount_a: float
    amount_b: float
    amount_c: float

    def get_agency_shortcut(self):
        return self.agency_shortcut

    def get_filing_id(self):
        return self.filing_id

    def get_filer_local_id(self):
        return self.filer_local_id

    def get_filer_id(self):
        return self.filer_id

    @staticmethod
    def is_filer_id_valid(filer_id: str):
        return filer_id.isdigit()
