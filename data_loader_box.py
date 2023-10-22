import ipywidgets as widgets
from ipywidgets import HBox, VBox

from src.netfile.agency.agencies import Agencies
from filing import add_all_agency_filings, get_years, get_filers
from summary import add_all_agency_year_summaries
from transaction import add_all_filer_filer_id_transactions


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
        self.filer_select_drop_down = widgets.Dropdown(
            description='Filer',
            disabled=True,
        )
        self.load_filer_transactions_button = widgets.Button(
            description="Load Transactions",
            disabled=True
        )

        row_a = HBox([self.load_agencies_button])
        row_b = HBox(
            [self.agency_select_drop_down, self.load_filings_button])
        row_c = HBox(
            [self.filing_years_select_drop_down, self.load_agency_summaries_button])
        row_d = HBox(
            [self.filer_select_drop_down, self.load_filer_transactions_button])
        self.layout = VBox([row_a, row_b, row_c, row_d])

        self.agencies = Agencies()

        self.add_events()
        self.update_agency_select_drop_down()

    def on_load_agencies_button_clicked(self, b):
        print('on_load_agencies_button_clicked 1')
        self.agencies.add_all_agencies()
        self.update_agency_select_drop_down()
    
    def update_agency_select_drop_down(self):
        agencies = self.agencies.get_all()
        if len(agencies) < 1:
            return

        agency_tups = [('Select City/County', 'none')]

        for agency_dict in agencies:
            agency_tups.append((agency_dict['name'], agency_dict['shortcut']))

        self.agency_select_drop_down.disabled = len(agencies) < 1
        self.agency_select_drop_down.options = agency_tups
        self.agency_select_drop_down.value = 'none'

    def on_agency_select_changed(self, change):
        self.load_filings_button.disabled = (change.new == 'none')
        self.update_year_select_drop_down(change.new)
        self.update_filer_select_drop_down(change.new)

    def on_load_filings_button_clicked(self, b):
        print('on_load_filings_button_clicked 1')
        agency_shortcut = self.agency_select_drop_down.value
        add_all_agency_filings(agency_shortcut)
        self.update_year_select_drop_down(agency_shortcut)
        self.update_filer_select_drop_down(agency_shortcut)
        
    def update_year_select_drop_down(self, agency_shortcut):
        if (agency_shortcut == 'none'):
            return
        years = get_years(agency_shortcut)
        years = sorted(list(set(years)), reverse=True)
        self.filing_years_select_drop_down.disabled = len(years) < 1

        if (len(years) > 0):
            self.filing_years_select_drop_down.options = ['select'] + years
            self.filing_years_select_drop_down.value = 'select'
        else:
            self.filing_years_select_drop_down.options = []
            self.filing_years_select_drop_down.value = None

    def update_filer_select_drop_down(self, agency_shortcut):
        if (agency_shortcut == 'none'):
            return
        filers = get_filers(agency_shortcut)
        self.filer_select_drop_down.disabled = len(filers) < 1
    
        sorted_filers = sorted(filers, key=lambda x: x['filerName'])

        filer_tups = [('Select Filer/Committee', 'none')]

        for filer_dict in sorted_filers:
            filer_tups.append((filer_dict['filerName'], filer_dict['filerLocalId']))

        if (len(filers) > 0):
            self.filer_select_drop_down.options = filer_tups
            self.filer_select_drop_down.value = 'none'
        else:
            self.filer_select_drop_down.options = []
            self.filer_select_drop_down.value = None

    def on_filing_years_select_changed(self, change):
        self.load_agency_summaries_button.disabled = (change.new == 'select')

    def on_filer_select_changed(self, change):
        self.load_filer_transactions_button.disabled = (change.new == 'none')

    def on_load_agency_summaries_button_clicked(self, b):
        print('on_load_agency_summaries_button_clicked 1')

        self.summary_list = []
        agency_shortcut = self.agency_select_drop_down.value
        filing_year = self.filing_years_select_drop_down.value
        add_all_agency_year_summaries(agency_shortcut, filing_year)

    def on_load_filer_transactions_button_clicked(self, b):
        print('on_load_filer_transactions_button_clicked 1')
        agency_shortcut = self.agency_select_drop_down.value
        filer_local_id = self.filer_select_drop_down.value
        print('filer_local_id', filer_local_id)
        add_all_filer_filer_id_transactions(agency_shortcut, filer_local_id)

    def add_events(self):
        self.load_agencies_button.on_click(self.on_load_agencies_button_clicked)
        self.agency_select_drop_down.observe(self.on_agency_select_changed, 'value')
        self.load_filings_button.on_click(self.on_load_filings_button_clicked)
        self.filing_years_select_drop_down.observe(self.on_filing_years_select_changed, 'value')
        self.load_agency_summaries_button.on_click(self.on_load_agency_summaries_button_clicked)
        self.filer_select_drop_down.observe(self.on_filer_select_changed, 'value')
        self.load_filer_transactions_button.on_click(self.on_load_filer_transactions_button_clicked)
