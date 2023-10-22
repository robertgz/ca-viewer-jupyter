import requests

# function to request a page of filings from NetFile
def get_filings(agencyShortcut: str, page=0):
    filing_url = 'https://www.netfile.com/Connect2/api/public/list/filing'
    payload = {
        "AID": agencyShortcut,
        "Application": "Campaign",
        "CurrentPageIndex": page,
        # Form 30 is for FPPC 460 
        # FPPC 460 forms should be the only forms that have summaries
        "Form": 30,
        'PageSize': '1000',
        "format": "json",
    }
    print(f'FILING: Requesting url: {filing_url}, with params: {payload}')
    response = requests.get(filing_url, params=payload, timeout=20)
    # The request intermittently stalls
    print(f'FILING: Requested url: {response.url}')
    return response.json()

# generator function to get each page of filings for an agency
def download_all_filings_gen_func(agencyShortcut: str):
    pageNumber = 0
    getNextPage = True

    while getNextPage:
        json = get_filings(agencyShortcut, pageNumber)
        if (len(json['filings']) < 1):
            return

        yield json['filings']

        pageNumber += 1
        getNextPage = json['totalMatchingPages'] > pageNumber

# function to get all pages of filings for an agency
# @deprecated('use filings.add_all_agency_filings')
def get_all_agency_filings(agencyShortcut: str):
    filing_list = []
    try:
        for filings in download_all_filings_gen_func(agencyShortcut):
            filing_list += filings
        return filing_list
    except requests.exceptions.Timeout as e:
        print('FILING:: Warning slow response from provider. \nThis issue is usually temporary. Try again in a few minutes. ')
        return []
