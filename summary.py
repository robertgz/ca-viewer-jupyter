import requests

# function to request a page of summaries from NetFile
def get_summary_year(agencyShortcut, year, page=0):
    summary_url = 'https://www.netfile.com/Connect2/api/public/campaign/export/cal201/summary/year'
    payload = {
        "AID": agencyShortcut,
        "year": year,
        "CurrentPageIndex": page,
        "PageSize": "1000",
        "ShowSuperceded": False,
        "format": "json",
    }
    response = requests.get(summary_url, params=payload)

    response_json = response.json()

    if (response_json["responseStatus"] != None and
        response_json["responseStatus"]["errorCode"] == 'SqlException'):
        # print(f'SUMMARY: Slow response from provider try again.')
        raise ResourceWarning("SUMMARY: Warning slow response from provider. \nThis issue is usually temporary. Try again in a few minutes.")

    print(f'SUMMARY: Request url: {response.url}')
    return response_json

# generator function to get each page of summaries for an agency and year
def download_all_summaries_year_gen_func(agencyShortcut, year):
    pageNumber = 0
    getNextPage = True

    while getNextPage:
        json = get_summary_year(agencyShortcut, year, pageNumber)
#         if (len(json['results']) < 1):
#             return;

        yield json['results']

        pageNumber += 1
        getNextPage = json['totalMatchingPages'] > pageNumber

# function to get all pages of summaries for an agency and year
def get_all_agency_year_summaries(agencyShortcut, year):
    summary_list = []
    try:
        for summaries in download_all_summaries_year_gen_func(agencyShortcut, year):
            summary_list += summaries
    except ResourceWarning as e:
        print(e)
    return summary_list
