import requests

# function to request a page of filings from NetFile
def get_filings(agencyShortcut, page=0):
    filing_url = 'https://www.netfile.com/Connect2/api/public/list/filing'
    payload = {
        "AID": agencyShortcut,
        "Application": "Campaign",
        "CurrentPageIndex": page,
        'PageSize': '1000',
        "format": "json",
    }
    response = requests.get(filing_url, params=payload)
    print(f'FILING: Request url: {response.url}')
    return response.json()

# generator function to get each page of filings for an agency
def download_all_filings_gen_func(agencyShortcut):
    pageNumber = 0
    getNextPage = True

    while getNextPage:
        json = get_filings(agencyShortcut, pageNumber)
        if (len(json['filings']) < 1):
            return;

        yield json['filings']

        pageNumber += 1
        getNextPage = json['totalMatchingPages'] > pageNumber

# function to get all pages of filings for an agency
def get_all_agency_filings(agencyShortcut):
    filing_list = []
    for filings in download_all_filings_gen_func(agencyShortcut):
        filing_list += filings
    return filing_list

# Filter by 'FPPC Form 460 Recipient Committee Campaign Statement' filngs
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

# Add a year field to each filing based on the title field
def add_filing_year(filings):
    for i in filings:
        i['year'] = get_year_from_title(i['title'])
    return filings
