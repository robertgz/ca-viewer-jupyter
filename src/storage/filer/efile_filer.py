from dataclasses import dataclass

import pandas as pd

from src.storage.filer.base_filer import BaseFiler

@dataclass(kw_only=True)
class EFileFiler(BaseFiler):
    Filer_NamL: str
    Filer_ID: str

    def get_name(self) -> str:
        return self.Filer_NamL

    def get_id(self) -> str:
        return self.Filer_ID
    
    @staticmethod
    def get_converter():
        return {col: str for col in ['Filer_ID']}

    @staticmethod
    def get_filers(df: pd.DataFrame):
        filers = df.filter(items=['Filer_ID', 'Filer_NamL']).drop_duplicates().to_dict('records')
        return [EFileFiler(**filer) for filer in filers]
    