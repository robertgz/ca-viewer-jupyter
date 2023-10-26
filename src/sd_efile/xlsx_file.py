from dataclasses import dataclass

@dataclass
class XLSXFile():
    agency_shortcut: str
    year: str
    filename: str
    url: str

    def get_year(self):
        return self.year

    def get_filename(self):
        return self.filename

    def get_url(self):
        return self.url
