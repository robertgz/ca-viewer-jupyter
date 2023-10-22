import requests

# Downloading an XLSX file requires two requests.
# The First request to 'efile.sandiego.gov' gets the url of the file. 
# A Second request is used to download the xlsx file using the location
# returned from the first request. 

def request_download_url(year: str,  most_recent = True):
    bulk_export_url = 'https://efile.sandiego.gov/api/v1/public/campaign-bulk-export-url'

    payload = {
        "year": year,
        "most_recent_only": most_recent,
    }
    response = requests.get(bulk_export_url, params=payload, timeout=20)
    return response.json()

def _get_data_from_url(year: str,  most_recent = True):
    json_response = request_download_url(year, most_recent)
    return json_response['data']

def download_file(url: str):
    response = requests.get(url, timeout=20)
    return response.content
