import os
import datetime

import download as sd_download

_year_files_list = []

def _get_filename(url: str):
    return url.split('/')[-1]

def init_years(agency_shortcut = 'CSD_EFILE'):
    year_limit = 2000
    global _year_files_list

    if (len(_year_files_list) > 1):
        return

    current_year = datetime.datetime.today().strftime('%Y')
    year = int(current_year)

    year_found = True
    while year_found and year > year_limit:
        json_response = sd_download.request_download_url(year)

        if 'success' in json_response:
            dirname = os.path.dirname(__file__)
            sub_directory = 'downloads'
            path = os.path.join(dirname, sub_directory)

            _year_files_list.append(
                {
                    'agency_shortcut': agency_shortcut,
                    'year': str(year),
                    'path': path,
                    'filename': _get_filename(json_response['data']),
                    'url': json_response['data'],
                }
            )
        else:
            year_found = False
        year -= 1

def _get_years_by_agency(agency_shortcut):
    global _year_files_list
    filtered = list(
        filter(lambda x: x['agency_shortcut'] == agency_shortcut, _year_files_list))
    return filtered

def get_years(agency_shortcut = 'CSD_EFILE'):
    agency_year_files_list = _get_years_by_agency(agency_shortcut)
    years = list(map(lambda x: x['year'], agency_year_files_list))
    return years

def get_year_item(year: str, agency_shortcut = 'CSD_EFILE'):
    global _year_files_list
    if len(_year_files_list) < 1:
        print('run init_years() first')
        return
    agency_year_files_list = _get_years_by_agency(agency_shortcut)
    filtered_year_items = list(filter(lambda x: x['year'] == year, agency_year_files_list))
    return filtered_year_items[0]

def conditionally_download(year_item):
    filepath = os.path.join(year_item['path'], year_item['filename'])
    found_locally = os.path.isfile(filepath)

    if not found_locally:
        path = year_item['path']
        if not os.path.exists(path):
            os.makedirs(path)
        sd_download.download_xlsx_year_to_file(filepath, year_item['url'])

    return filepath
