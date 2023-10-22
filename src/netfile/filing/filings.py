from requests import exceptions
import pandas as pd

from . import download as filing_download

def get_unique_list(input_list):
    return pd.DataFrame(input_list).drop_duplicates().to_dict('records')

class Filings:
    def __init__(self):
        self.filing_list = []
    
    def get_filter_filings(self, input_filings):
        ids = list(map(lambda x: x['id'], self.filing_list))
        return list(filter(lambda x: x['id'] not in ids, input_filings))

    def filter_out_non_e_filed(self, input_filings):
        return list(filter(lambda x: x['isEfiled'] == True, input_filings))

    def add_filings(self, agency_shortcut: str, input_filings):
        unique_filings = get_unique_list(input_filings)

        filings_to_add = self.get_filter_filings(unique_filings)
        filings_to_add = self.filter_out_non_e_filed(filings_to_add)
        
        filings_with_fields = self.add_fields(agency_shortcut, filings_to_add)
        self.filing_list += filings_with_fields

        return filings_with_fields
    
    def add_all_agency_filings(self, agencyShortcut: str):
        try:
            for filings in filing_download.download_all_filings_gen_func(agencyShortcut):
                self.add_filings(agencyShortcut, filings)

        except (exceptions.Timeout, ConnectionError) as e:
            print('FILING:: Warning slow response from provider. \nThis issue is usually temporary. Try again in a few minutes. ')

    def get_filings(self, agencyShortcut: str):
        return list(filter(lambda x: x['agencyShortcut'] == agencyShortcut, self.filing_list))

    def get_years(self, agencyShortcut: str):
        agency_filings = self.get_filings(agencyShortcut)
        return list(map(lambda x: x['year'], agency_filings))
    
    def get_filers(self, agency_shortcut: str):
        filings = list(filter(lambda x: x['agencyShortcut'] == agency_shortcut, self.filing_list))

        filers = []
        for i in filings:
            filers.append({"filerName": i['filerName'], "filerLocalId": i['filerLocalId']})

        return get_unique_list(filers)

    # Add a year field to each filing based on the title field
    def add_fields(self, agency_shortcut, filings):
        for i in filings:
            i['year'] = self.get_year_from_filing(i)
            i['agencyShortcut'] = agency_shortcut
        return filings

    # Filter by 'FPPC Form 460 Recipient Committee Campaign Statement' filings
    # The 460 filings should be the only forms that have summaries
    # form 460 is indicated by the field 'form' with a value of 30
    # For a list of form types see: https://www.netfile.com/Connect2/api/public/list/form/types
    def get_summary_filings(self, filings):
        # Form 30 is for FPPC 460, this should be the only form that has summaries
        forms_list = [30]
        result = filter(lambda filing: filing['form'] in forms_list, filings)
        return list(result)

    # Filings that are not eFiled will not have summaries
    # Only filings that are eFiled can have summaries
    def get_efiled_filings(self, filings):
        isEfiledCondition = True
        result = filter(lambda filing: filing['isEfiled'] == isEfiledCondition, filings)
        return list(result)




    # Derive a the year from an input string
    # An example input string: 'FPPC Form 460 (1/1/2023 - 9/23/2023)'
    # The resulting year: '2023'
    def get_year_from_title(self, title):
        try:
            year = title.partition(' (')[2].partition('-')[0].strip().split('/')[2]
            return year
        except Exception as e:
            print(f'Title not able to be parsed: {title}')
            return ''

    def get_year_from_filing(self, filing):
        try:
            year = filing['title'].partition(' (')[2].partition('-')[0].strip().split('/')[2]
            return year
        except Exception as e:
            print(f'Title not able to be parsed: {filing["title"]}, id: {filing["id"]}')
            return ''

    # Add a year field to each filing based on the title field
    # @deprecated('use add_fields')
    def add_filing_year(self, filings):
        for i in filings:
            i['year'] = self.get_year_from_title(i['title'])
        return filings

    def get_customized_filings(self, filings):
        new_filings = self.get_summary_filings(filings)
        new_filings = self.get_efiled_filings(new_filings)
        new_filings = self.add_filing_year(new_filings)
        return new_filings

    def get_years_from_filings(self, filings):
        years = []
        for filing in self.get_customized_filings(filings):
            years.append(filing['year'])
        return years
