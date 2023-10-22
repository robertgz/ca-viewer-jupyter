
def convert_to_common(summaries):
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
