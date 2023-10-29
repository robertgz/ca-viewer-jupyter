from dataclasses import dataclass

from src.storage.filer.base_filer import BaseFiler

@dataclass(kw_only=True)
class EFileFiler(BaseFiler):
    Filer_NamL: str
    Filer_ID: str

    def get_name(self) -> str:
        return self.Filer_NamL

    def get_id(self) -> str:
        return self.Filer_ID
    