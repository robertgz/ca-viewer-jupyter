import requests
import datetime

summary_sheet_name = 'F460-Summary'

def _request_download_url(year: str,  most_recent = True):
    bulk_export_url = 'https://efile.sandiego.gov/api/v1/public/campaign-bulk-export-url'

    payload = {
        "year": year,
        "most_recent_only": most_recent,
    }
    # print(f'EFILE: Requesting download url: {bulk_export_url}, with params: {payload}')
    response = requests.get(bulk_export_url, params=payload, timeout=20)
    # print(f'FILING: Requested url: {response.url}')
    return response.json()

def get_download_url(year: str,  most_recent = True):
    json_response = _request_download_url(year, most_recent)
    return json_response['data']

def _get_filename(url: str):
    return url.split('/')[-1]

def download_xlsx_to_file(url: str):
    filename = _get_filename(url)
    response = requests.get(url, timeout=20)
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename
