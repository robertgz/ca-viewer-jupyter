from summary_download import download_all_summaries_year_gen_func

# function to get all pages of summaries for an agency and year
def get_all_agency_year_summaries(agencyShortcut, year):
    summary_list = []
    try:
        for summaries in download_all_summaries_year_gen_func(agencyShortcut, year):
            summary_list += summaries
    except ResourceWarning as e:
        print(e)
    return summary_list
