
from typing import List

from .common_summary import CommonSummary

class CommonSummaries():
    def __init__(self):
        self.common_summaries: List[CommonSummary] = []

    @staticmethod
    def _get_new_filing_ids(input_summaries: List[CommonSummary], existing_summaries: List[CommonSummary]):
        input_ids = set([x.get_filing_id() for x in input_summaries])
        existing_ids = set([x.get_filing_id() for x in existing_summaries])
        return list(input_ids.difference(existing_ids))

    @staticmethod
    def _get_duplicate_filing_ids(input_summaries: List[CommonSummary], existing_summaries: List[CommonSummary]):
        input_ids = set([x.get_filing_id() for x in input_summaries])
        existing_ids = set([x.get_filing_id() for x in existing_summaries])
        return list(input_ids.intersection(existing_ids))

    @staticmethod
    def _get_updatable_filing_ids(
        filing_ids: list[str],
        input_summaries: List[CommonSummary],
        existing_summaries: List[CommonSummary],
    ):
        updatable_filing_ids: list[str] = []

        # Note that there is a difference between a filing_id and a filer_id
        # A filer is a person or committee that creates filings
        for id in filing_ids:
            input_filer_id = next(
                x for x in input_summaries if x.get_filing_id() == id).get_filing_id()
            existing_filer_id = next(
                x for x in existing_summaries if x.get_filing_id() == id).get_filing_id()

            if CommonSummary.is_filer_id_valid(existing_filer_id) or existing_filer_id == input_filer_id:
                continue
            elif CommonSummary.is_filer_id_valid(input_filer_id):
                updatable_filing_ids.append(id)

        return updatable_filing_ids
    

    def add(self, summaries):
        input_summaries = [CommonSummary(**summary) for summary in summaries]
        new_ids = self._get_new_filing_ids(input_summaries, self.common_summaries)

        if len(new_ids) > 0:
            new_summaries = [x for x in input_summaries if x.get_filing_id() in new_ids]
            self.common_summaries += new_summaries

        duplicate_ids = self._get_duplicate_filing_ids(input_summaries, self.common_summaries)

        if len(duplicate_ids) > 0:            
            ids_to_replace = self._get_updatable_filing_ids(
                duplicate_ids, input_summaries, self.common_summaries)

            if len(ids_to_replace) > 0:
                self.remove(ids_to_replace)
                summaries_to_add = [x for x in input_summaries if x.get_filing_id() in ids_to_replace]
                self.common_summaries += summaries_to_add

    def remove(self, filing_ids: List[str]):
        self.common_summaries = [
            x for x in self.common_summaries if x.get_filing_id() in filing_ids]

    def get_by_agency(self, agency_shortcut: str):
        return [x for x in self.common_summaries if x.get_agency_shortcut().capitalize() == agency_shortcut.capitalize()]

    def get_by_filer(self, filer_id: str):
        return [x for x in self.common_summaries if x.get_filer_id() == filer_id]

    def get_by_local_filer(self, filer_local_id: str):
        return [x for x in self.common_summaries if x.get_filer_local_id() == filer_local_id]
