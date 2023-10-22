from ...netfile.filing import filings

def test_get_unique_filings_1():
    test_filings = [
        { 'id': 'test_1', 'filerName': 'Filer name 1' },
        { 'id': 'test_2', 'filerName': 'Filer name 2' },
        { 'id': 'test_3', 'filerName': 'Filer name 3' },
        { 'id': 'test_3', 'filerName': 'Filer name 3' },
        { 'id': 'test_4', 'filerName': 'Filer name 4' },
        { 'id': 'test_4', 'filerName': 'Filer name 4' },
    ]
    response_filings = filings.get_unique_list(test_filings)
    assert len(response_filings) == 4

def test_get_filter_filings_1():
    filing = filings.Filings()
    filing.filing_list = []
    test_filings = [
        { 'id': 'test_1', 'filerName': 'Filer name 1' },
        { 'id': 'test_2', 'filerName': 'Filer name 2' },
    ]
    filtered = filing.get_filter_filings(test_filings)
    assert len(filtered) == len(test_filings)

def test_get_filter_filings_2():
    filing = filings.Filings()
    filing.filing_list = [
        { 'id': 'test_1', 'filerName': 'Filer name 1' },
        { 'id': 'test_2', 'filerName': 'Filer name 2' },
    ]
    test_filings = [
        { 'id': 'test_2', 'filerName': 'Filer name 2' },
        { 'id': 'test_3', 'filerName': 'Filer name 3' },
    ]

    filtered = filing.get_filter_filings(test_filings)
    assert len(filtered) == 1
    assert filtered[0]['id'] == 'test_3'

def test_get_year_from_title_1():
    filing = filings.Filings()
    title = 'FPPC Form 460 (10/18/2020 - 12/31/2020)'
    result = filing.get_year_from_title(title)
    assert result == '2020'

def test_get_year_from_title_2():
    filing = filings.Filings()
    title = 'FPPC Form 460 (10/18/2020 - )'
    result = filing.get_year_from_title(title)
    assert result == '2020'

def test_get_year_from_title_3():
    filing = filings.Filings()
    title = 'FPPC Form 460 ( - 12/31/2020)'
    result = filing.get_year_from_title(title)
    assert result == ''

# def test__add_fields_1():

def test_add_filings_1():
    filing = filings.Filings()
    filing.filing_list = []
    agency_shortcut = 'test_agency'

    test_filings1 = [
        {'id': 'test_1', 'filerName': 'Filer name 1',
            'title': 'FPPC Form 460 (10/18/2020 - 12/31/2020)', 'isEfiled': True},
    ]

    test_filings2 = [
        {'id': 'test_2', 'filerName': 'Filer name 2',
            'title': 'FPPC Form 460 (10/18/2020 - 12/31/2020)', 'isEfiled': True},
        {'id': 'test_3', 'filerName': 'Filer name 3',
            'title': 'FPPC Form 460 (10/18/2020 - 12/31/2020)', 'isEfiled': True},
    ]

    test_filings3 = [
        {'id': 'test_3', 'filerName': 'Filer name 3',
            'title': 'FPPC Form 460 (10/18/2020 - 12/31/2020)', 'isEfiled': True},
    ]

    filing.add_filings(agency_shortcut, test_filings1)
    filing.add_filings(agency_shortcut, test_filings2)
    filing.add_filings(agency_shortcut, test_filings3)
    assert len(filing.filing_list) == 3
    assert filing.filing_list[0]['agencyShortcut'] == agency_shortcut
