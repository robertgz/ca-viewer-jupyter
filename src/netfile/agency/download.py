import requests
from typing import TypedDict, Optional

from ..response_status_type import NetFileResponseStatus

class NetFileDownloadedAgency(TypedDict):
    id: int
    shortcut: str
    name: str

class NetFileDownloadedAgencyResponse(TypedDict):
    agencies: NetFileDownloadedAgency
    responseStatus: Optional[NetFileResponseStatus]

agencies_url = 'https://www.netfile.com/Connect2/api/public/campaign/agencies.json'

# Request the agency list from NetFile
def download_agencies() -> NetFileDownloadedAgencyResponse:
    global agencies_url
    response = requests.get(agencies_url)

    print(f'AGENCY: Request url: {response.url}')
    return response.json()
