from requests import exceptions
import pandas as pd
from transaction_download import download_all_transaction_filer_gen_func

_transaction_list = []

def add_all_filer_filer_id_transactions(agency_shortcut: str, filer_local_id: str):
    try:
        for transactions in download_all_transaction_filer_gen_func(filer_local_id):
            _add_transactions(agency_shortcut, transactions)

    except exceptions.Timeout as e:
        print('SUMMARY: Warning slow response from provider. \nThis issue is usually temporary. Try again in a few minutes. ')

def _add_transactions(agency_shortcut: str, input_transactions):
    unique_transactions = _get_unique_transactions(input_transactions)

    global _transaction_list
    transaction_to_add = _get_new_transactions(unique_transactions)

    transaction_with_fields = _add_fields(agency_shortcut, transaction_to_add)
    _transaction_list += transaction_with_fields

    return transaction_with_fields

def _get_unique_transactions(input_transactions):
    return pd.DataFrame(input_transactions).drop_duplicates().to_dict('records')

def _get_new_transactions(input_transactions):
    global _transaction_list
    netFileKeys = list(map(lambda x: x['netFileKey'], _transaction_list))
    new_transaction_list= list(filter(lambda x: x['netFileKey'] not in netFileKeys, input_transactions))
    return new_transaction_list

def _add_fields(agency_shortcut, transactions):
    for i in transactions:          
        i['year'] = _get_year_from_transaction(i)
        i['agencyShortcut'] = agency_shortcut
    return transactions

def _get_year_from_transaction(transaction):
    year = None
    if len(transaction['tran_Date']) > 0:
        year = transaction['tran_Date'].partition('-')[0]
    elif len(transaction['calculated_Date']) > 0:
        year = transaction['calculated_Date'].partition('-')[0]
    return year
