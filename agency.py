import requests

# Request the agency list from NetFile
def download_agencies():
    agencies_url = 'https://www.netfile.com/Connect2/api/public/campaign/agencies.json'
    response = requests.get(agencies_url)

    print(f'AGENCY: Request url: {response.url}')
    return response.json()

# Add isCounty flag to each agency
def detect_counties(agencies):
    for i in agencies:
        i['isCounty'] = 'County' in i['name']
    return agencies

# Filter out unneeded agencies
def remove_extra_agencies(agencies):
    skip_list = ['SUPER', 'CA', 'COR_bak', 'SFO']
    result = filter(lambda temp: temp['shortcut'] not in skip_list, agencies)
    return list(result)

# Run the above functions
def get_agency_list():
    agency_response = download_agencies()
    agencies = agency_response['agencies']    
    agencies = detect_counties(agencies)
    agencies = remove_extra_agencies(agencies)
    return agencies
