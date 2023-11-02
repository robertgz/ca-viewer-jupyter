import requests
from typing import TypedDict, Optional

from ..response_status_type import NetFileResponseStatus

class NetFileDownloadedFiling(TypedDict):
    id: str
    agency: int
    isEfiled: bool
    hasImage: bool
    filingDate: str
    title: str
    form: int
    filerName: str
    filerLocalId: str
    filerStateId: str
    amendmentSequenceNumber: int
    amendedFilingId: str

class NetFileDownloadedFilingResponse(TypedDict):
    filings: list[NetFileDownloadedFiling]
    responseStatus: Optional[NetFileResponseStatus]
    totalMatchingCount: int
    totalMatchingPages: int

# function to request a page of filings from NetFile
def get_filings(agency_shortcut: str, page=0, form: int = None) -> NetFileDownloadedFilingResponse:
    filing_url = 'https://www.netfile.com/Connect2/api/public/list/filing'
    payload = {
        "AID": agency_shortcut,
        "Application": "Campaign",
        "CurrentPageIndex": page,
        # Form 30 is for FPPC 460 
        # FPPC 460 forms should be the only forms that have summaries
        "Form": form,
        'PageSize': '1000',
        "format": "json",
    }
    print(f'FILING: Requesting url: {filing_url}, with params: {payload}')
    response = requests.get(filing_url, params=payload, timeout=20)
    # The request intermittently stalls
    print(f'FILING: Requested url: {response.url}')
    return response.json()

# generator function to get each page of filings for an agency
def download_all_filings_gen_func(agency_shortcut: str, form: int = None):
    pageNumber = 0
    getNextPage = True

    while getNextPage:
        json = get_filings(agency_shortcut, pageNumber, form)
        if (len(json['filings']) < 1):
            return

        yield json['filings']

        pageNumber += 1
        getNextPage = json['totalMatchingPages'] > pageNumber

def get_all_agency_filings(agency_shortcut: str, form: int = None) -> list[NetFileDownloadedFiling]:
    filing_list = []
    try:
        for filings in download_all_filings_gen_func(agency_shortcut, form):
            filing_list += filings
        return filing_list
    except (requests.exceptions.Timeout, ConnectionError) as e:
        print('FILING:: Warning slow response from provider. \nThis issue is usually temporary. Try again in a few minutes. ')
        return []
