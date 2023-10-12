from requests import exceptions
import pandas as pd
from typing import TypeAlias
from filing_download import download_all_filings_gen_func

_filing_list = []

FilingDownload: TypeAlias = dict[any]

def get_unique_filings(input_filings: list(FilingDownload)):
    return pd.DataFrame(input_filings).drop_duplicates().to_dict('records')

def get_filter_filings(input_filings: list(FilingDownload)):
    global _filing_list
    ids = list(map(lambda x: x['id'], _filing_list))
    new_filing_list = list(filter(lambda x: x['id'] not in ids, input_filings))
    return new_filing_list

def filter_out_non_e_filed(input_filings: list(FilingDownload)):
    return list(filter(lambda x: x['isEfiled'] == True, input_filings))

def add_filings(agency_shortcut: str, input_filings: list(FilingDownload)):
    unique_filings = get_unique_filings(input_filings)

    global _filing_list
    filings_to_add = get_filter_filings(unique_filings)
    filings_to_add = filter_out_non_e_filed(filings_to_add)
    
    filings_with_fields = _add_fields(agency_shortcut, filings_to_add)
    _filing_list += filings_with_fields

    return filings_with_fields

def add_all_agency_filings(agencyShortcut: str):
    try:
        for filings in download_all_filings_gen_func(agencyShortcut):
            add_filings(agencyShortcut, filings)

    except exceptions.Timeout as e:
        print('FILING:: Warning slow response from provider. \nThis issue is usually temporary. Try again in a few minutes. ')

def get_filings(agencyShortcut: str):
    global _filing_list
    filings = list(filter(lambda x: x['agencyShortcut'] == agencyShortcut, _filing_list))
    return filings

def get_years(agencyShortcut: str):
    agency_filings = get_filings(agencyShortcut)
    years = list(map(lambda x: x['year'], agency_filings))
    return years

# Add a year field to each filing based on the title field
def _add_fields(agency_shortcut, filings):
    for i in filings:
        i['year'] = _get_year_from_filing(i)
        i['agencyShortcut'] = agency_shortcut
    return filings

# Filter by 'FPPC Form 460 Recipient Committee Campaign Statement' filings
# The 460 filings should be the only forms that have summaries
# form 460 is indicated by the field 'form' with a value of 30
# For a list of form types see: https://www.netfile.com/Connect2/api/public/list/form/types
def get_summary_filings(filings):
    # Form 30 is for FPPC 460, this should be the only form that has summaries
    forms_list = [30]
    result = filter(lambda filing: filing['form'] in forms_list, filings)
    return list(result)

# Filings that are not eFiled will not have summaries
# Only filings that are eFiled can have summaries
def get_efiled_filings(filings):
    isEfiledCondition = True
    result = filter(lambda filing: filing['isEfiled'] == isEfiledCondition, filings)
    return list(result)

# Derive a the year from an input string
# An example input string: 'FPPC Form 460 (1/1/2023 - 9/23/2023)'
# The resulting year: '2023'
def get_year_from_title(title):
    try:
        year = title.partition(' (')[2].partition('-')[0].strip().split('/')[2]
        return year
    except Exception as e:
        print(f'Title not able to be parsed: {title}')
        return ''

def _get_year_from_filing(filing):
    try:
        year = filing['title'].partition(' (')[2].partition('-')[0].strip().split('/')[2]
        return year
    except Exception as e:
        print(f'Title not able to be parsed: {filing["title"]}, id: {filing["id"]}')
        return ''

# Add a year field to each filing based on the title field
# @deprecated('use add_fields')
def add_filing_year(filings):
    for i in filings:
        i['year'] = get_year_from_title(i['title'])
    return filings

def get_customized_filings(filings):
    new_filings = get_summary_filings(filings)
    new_filings = get_efiled_filings(new_filings)
    new_filings = add_filing_year(new_filings)
    return new_filings

def get_years_from_filings(filings):
  years = []
  for filing in get_customized_filings(filings):
    years.append(filing['year'])
  return years
