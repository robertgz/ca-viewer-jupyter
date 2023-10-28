
from dataclasses import dataclass
from typing import List

@dataclass(kw_only=True)
class BaseAgency:
    def get_name() -> str:
        pass

    def get_agency_shortcut() -> str:
        pass

    def get_years() -> List[str]:
        pass

    @staticmethod
    def get_agencies():
        pass

    