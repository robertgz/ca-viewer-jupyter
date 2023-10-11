import ipywidgets as widgets
from ipywidgets import HBox, VBox

from agency import get_agency_list
from filing import get_years_from_filings, add_all_agency_filings, get_filings
from filing_download import get_all_agency_filings
from summary import get_all_agency_year_summaries


class DataLoaderBox:
    def __init__(self):
        self.load_agencies_button = widgets.Button(
            description="Load Agency list",
        )
        self.agency_select_drop_down = widgets.Dropdown(
            description='Agency',
            disabled=True,
        )
        self.load_filings_button = widgets.Button(
            description="Load Filings",
            disabled=True
        )
        self.filing_years_select_drop_down = widgets.Dropdown(
            description='Year',
            disabled=True,
        )
        self.load_agency_summaries_button = widgets.Button(
            description="Load Summaries",
            disabled=True
        )

        row_a = HBox([self.load_agencies_button])
        row_b = HBox(
            [self.agency_select_drop_down, self.load_filings_button])
        row_c = HBox(
            [self.filing_years_select_drop_down, self.load_agency_summaries_button])
        self.layout = VBox([row_a, row_b, row_c])

        self.add_events()

    def on_load_agencies_button_clicked(self, b):
        print('on_load_agencies_button_clicked 1')
        self.agencies = get_agency_list()
        print('on_load_agencies_button_clicked 2')
        self.update_agency_select_drop_down()
   
    def update_agency_select_drop_down(self):
        agency_tups = [('Select City/County', 'none')]

        for agency_dict in self.agencies:
            agency_tups.append((agency_dict['name'], agency_dict['shortcut']))

        self.agency_select_drop_down.disabled = len(self.agencies) < 1
        self.agency_select_drop_down.options = agency_tups
        self.agency_select_drop_down.value = 'none'

    def on_agency_select_changed(self, change):
        self.load_filings_button.disabled = (change.new == 'none')

    def on_load_filings_button_clicked(self, b):
        print('on_load_filings_button_clicked 1')

        self.filing_list = []

        agency_shortcut = self.agency_select_drop_down.value
        print('on_load_filings_button_clicked 2')

        add_all_agency_filings(agency_shortcut)
        self.filing_list = get_filings(agency_shortcut)
        print(f'Filings downloaded: {len(self.filing_list)}')
        
        if len(self.filing_list) < 1:
            return
        
        years = get_years_from_filings(self.filing_list)
        years = sorted(list(set(years)), reverse=True)

        self.filing_years_select_drop_down.disabled = len(years) < 1
        self.filing_years_select_drop_down.options = ['select'] + years
        self.filing_years_select_drop_down.value = 'select'

    def on_filing_years_select_changed(self, change):
        self.load_agency_summaries_button.disabled = (change.new == 'select')

    def on_load_agency_summaries_button_clicked(self, b):
        print('on_load_agency_summaries_button_clicked 1')

        self.summary_list = []
        agency_shortcut = self.agency_select_drop_down.value
        filing_year = self.filing_years_select_drop_down.value
        summaries_response_json = get_all_agency_year_summaries(agency_shortcut, filing_year)
        print(f'Number of summaries: {len(summaries_response_json)}, for year {filing_year}')
        self.summary_list = summaries_response_json

    def add_events(self):
        self.load_agencies_button.on_click(self.on_load_agencies_button_clicked)
        self.agency_select_drop_down.observe(self.on_agency_select_changed, 'value')
        self.load_filings_button.on_click(self.on_load_filings_button_clicked)
        self.filing_years_select_drop_down.observe(self.on_filing_years_select_changed, 'value')
        self.load_agency_summaries_button.on_click(self.on_load_agency_summaries_button_clicked)
