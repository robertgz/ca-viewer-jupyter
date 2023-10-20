
import pandas as pd
import sd_efile.summary_sd_efile_download as sdefile

summary_sheet_name = 'F460-Summary'

def _get_year_workbook(year_item):
    filepath = sdefile.conditionally_download(year_item)

    return pd.ExcelFile(filepath)

def get_sheet_names(year: str):
    item = sdefile.get_year_item(year)
    workbook = _get_year_workbook(item)
    return workbook.sheet_names

def get_year_summaries(year: str):
    item = sdefile.get_year_item(year)
    workbook = _get_year_workbook(item)

    global summary_sheet_name
    worksheet = workbook.parse(summary_sheet_name)
    summaries = worksheet.to_dict('records')
    return summaries

def convert_efile_summaries_to_common(summaries):
    new_summaries = []
    for summary in summaries:
        new_summaries.append(
            {
                'filer_local_id': None,
                'filer_id': summary['Filer_ID'],
                'filer_name': summary['Filer_NamL'],
                'filing_id': summary['e_filing_id'],
                "form_type": summary['Form_Type'],
                "line_item": summary['Line_Item'],
                "amount_a": summary['Amount_A'],
                "amount_b": summary['Amount_B'],
                "amount_c": summary['Amount_C'],
            }
        )
    return new_summaries
