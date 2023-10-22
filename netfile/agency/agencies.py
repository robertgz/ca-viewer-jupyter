
from . import download as agency_download

class Agencies:
    def __init__(self):
        self.agency_list = []
    
    def add(self, input_agencies):
        shortcuts = list(map(lambda x: x['shortcut'], self.agency_list))
        new_agency_list = filter(lambda x: x['shortcut'] not in shortcuts, input_agencies)
        agencies_to_add = list(new_agency_list)

        filtered_agency_list = self.remove_extra_agencies(agencies_to_add)
        updated_agency_list = self.add_county_flag(filtered_agency_list)

        self.agency_list += updated_agency_list

        return updated_agency_list

    # Filter out invalid agencies
    def remove_extra_agencies(self, agencies):
        skip_list = ['SUPER', 'CA', 'COR_bak', 'SFO']
        result = filter(lambda temp: temp['shortcut'] not in skip_list, agencies)
        return list(result)
    
    # Add isCounty (boolean) flag to each agency
    def add_county_flag(self, agencies):
        for i in agencies:
            i['isCounty'] = 'County' in i['name']
        return agencies
    
    def add_all_agencies(self):
        agency_response = agency_download.download_agencies()
        agencies = agency_response['agencies']
        self.add(agencies)
    
    def get_agency_list(self):
        if len(self.agency_list) < 1:
            agency_response = agency_download.download_agencies()
            agencies = agency_response['agencies']
            self.add(agencies)
        return self.get_all()

    def get_all(self):
        return self.agency_list

    def remove_all(self):
        self.agency_list = []
    