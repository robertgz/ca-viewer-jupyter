
from typing import List

from .base_agency import BaseAgency
from .netfile_agency import NetFileAgency
from .efile_agency import EFileAgency

class Agencies:
    def __init__(self):
        self.common_agencies: List[BaseAgency] = []
        self.net_file_agencies_loaded = False
        self.e_file_agencies_loaded = False
    
    def add_agencies(self):
        if not self.net_file_agencies_loaded:
            net_file_agencies = NetFileAgency.get_agencies()
            self.common_agencies.extend(net_file_agencies)
            self.net_file_agencies_loaded = True
        
        if not self.e_file_agencies_loaded:
            e_file_agencies = EFileAgency.get_agencies()
            self.common_agencies.extend(e_file_agencies)
            self.e_file_agencies_loaded = True

    def load_agencies(self, force=False):
        if not self.net_file_agencies_loaded or not self.e_file_agencies_loaded or force:
            self.add_agencies()

    def get_agencies(self):
        return self.common_agencies
