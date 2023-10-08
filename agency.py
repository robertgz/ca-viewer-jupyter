from agency_download import download_agencies

_agency_list = []

def add(input_agencies):
    global _agency_list
    shortcuts = list(map(lambda x: x['shortcut'], _agency_list))
    new__agency_list = filter(lambda x: x['shortcut'] not in shortcuts, input_agencies)
    agencies_to_add = list(new__agency_list)

    filtered__agency_list = _remove_extra_agencies(agencies_to_add)
    updated__agency_list = _add_county_flag(filtered__agency_list)

    _agency_list += updated__agency_list

    return updated__agency_list

def get_all():
    global _agency_list
    return _agency_list

def remove_all():
    global _agency_list
    _agency_list = []

# Add isCounty (boolean) flag to each agency
def _add_county_flag(agencies):
    for i in agencies:
        i['isCounty'] = 'County' in i['name']
    return agencies

# Filter out invalid agencies
def _remove_extra_agencies(agencies):
    skip_list = ['SUPER', 'CA', 'COR_bak', 'SFO']
    result = filter(lambda temp: temp['shortcut'] not in skip_list, agencies)
    return list(result)

def get_agency_list():
    if len(_agency_list)  < 1:
        agency_response = download_agencies()
        agencies = agency_response['agencies']
        add(agencies)
    return get_all()
