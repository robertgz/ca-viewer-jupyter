from requests import exceptions
import pandas as pd
from typing import TypeAlias
from .download import download_all_summaries_year_gen_func

_summary_list = []

SummaryDownload: TypeAlias = dict[any]

def add_all_agency_year_summaries(agency_shortcut, year):
    try:
        for summaries in download_all_summaries_year_gen_func(agency_shortcut, year):
            _add_summaries(agency_shortcut, summaries)

    except exceptions.Timeout as e:
        print('SUMMARY: Warning slow response from provider. \nThis issue is usually temporary. Try again in a few minutes. ')

def _add_summaries(agency_shortcut: str, input_summaries):
    unique_summaries = _get_unique_summaries(input_summaries)

    global _summary_list
    summaries_to_add = _get_new_summaries(unique_summaries)

    summaries_with_fields = _add_fields(agency_shortcut, summaries_to_add)
    _summary_list += summaries_with_fields

    return summaries_with_fields

def _get_unique_summaries(input_summaries: list(SummaryDownload)):
    return pd.DataFrame(input_summaries).drop_duplicates().to_dict('records')

def _get_new_summaries(input_summaries: list(SummaryDownload)):
    global _summary_list
    netFileKeys = list(map(lambda x: x['netFileKey'], _summary_list))
    new_summary_list = list(filter(lambda x: x['netFileKey'] not in netFileKeys, input_summaries))
    return new_summary_list
    
def _add_fields(agency_shortcut, summaries):
    for i in summaries:          
        i['year'] = _get_year_from_summary(i)
        i['agencyShortcut'] = agency_shortcut
    return summaries

def _get_year_from_summary(summary):
    year = None
    if len(summary['filingStartDate']) > 0:
        year = summary['filingStartDate'].partition('-')[0]
    elif len(summary['filingEndDate']) > 0:
        year = summary['filingEndDate'].partition('-')[0]
    return year        

# function to get all pages of summaries for an agency and year
def get_all_agency_year_summaries(agencyShortcut, year):
    summary_list = []
    try:
        for summaries in download_all_summaries_year_gen_func(agencyShortcut, year):
            summary_list += summaries
    except ResourceWarning as e:
        print(e)
    return summary_list
