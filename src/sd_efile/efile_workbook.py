import pandas as pd

class EFileWorkbook():
    def __init__(self, filepath):
        self.workbook = pd.ExcelFile(filepath)

    def get_filers(self):
        converter = {col: str for col in ['Filer_ID']}
        df = self.workbook.parse(
            'F460-Summary', converters=converter).filter(items=['Filer_ID', 'Filer_NamL'])
        return df.drop_duplicates().to_dict('records')
