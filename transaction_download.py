import requests

def _get_transaction_filer(filer_local_id: str, page=0):
    transaction_url = 'https://www.netfile.com/Connect2/api/public/campaign/export/cal201/transaction/filer'

    payload = {
        "FilerId": filer_local_id,
        "CurrentPageIndex": page,
        "PageSize": "1000",
        "ShowSuperceded": False,
        # "TransactionType": "",
        "format": "json",
    }

    response = requests.get(transaction_url, params=payload)

    response_json = response.json()

    if (response_json["responseStatus"] != None and
            response_json["responseStatus"]["errorCode"] == 'SqlException'):
        raise ResourceWarning(
            "SUMMARY: Warning slow response from provider. \nThis issue is usually temporary. Try again in a few minutes.")

    print(f'TRANSACTION: Request url: {response.url}')
    return response_json


def download_all_transaction_filer_gen_func(filer_local_id: str):
    pageNumber = 0
    getNextPage = True

    while getNextPage:
        json = _get_transaction_filer(filer_local_id, pageNumber)

        yield json['results']

        pageNumber += 1
        getNextPage = json['totalMatchingPages'] > pageNumber
