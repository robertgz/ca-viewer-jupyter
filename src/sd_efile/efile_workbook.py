import pandas as pd

class EFileWorkbook():
    def __init__(self, filepath):
        self.workbook = pd.ExcelFile(filepath)

    def get_sheet_Names(self):
        return self.workbook.sheet_names

    def get_summary_data_frame(self, converter) -> pd.DataFrame:
        return self.workbook.parse('F460-Summary', converters=converter)
