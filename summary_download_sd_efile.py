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

## Years
import os
_years_download = []

def init_years(agency_shortcut = 'CSD_EFILE'):
    year_limit = 2000
    global _years_download

    current_year = datetime.datetime.today().strftime('%Y')
    year = int(current_year)

    year_found = True
    while year_found and year > year_limit:
        json_response = _request_download_url(year)
        if 'success' in json_response:
            _years_download.append(
                {
                    'agency_shortcut': agency_shortcut,
                    'year': str(year),
                    'filename': _get_filename(json_response['data']),
                    'url': json_response['data'],
                }
            )
        else:
            year_found = False
        year -= 1

def _get_years_by_agency(agency_shortcut):
    global _years_download
    filtered = list(
        filter(lambda x: x['agency_shortcut'] == agency_shortcut, _years_download))
    return filtered

def get_downloadable_years(agency_shortcut = 'CSD_EFILE'):
    agency_years_download = _get_years_by_agency(agency_shortcut)
    years = list(map(lambda x: x['year'], agency_years_download))
    return years
