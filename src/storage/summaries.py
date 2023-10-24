
class Summaries:
    def __init__(self):
        self.summary_storage_list = []

    @staticmethod
    def get_filing_ids_set(summaries):
        return set(map(lambda x: x['filing_id'], summaries))

    def get_duplicate_filing_ids(self, summaries):
        ids_set = self.get_filing_ids_set(summaries)
        stored_ids_set = self.get_filing_ids_set(self.summary_storage_list)

        duplicate_ids = ids_set.intersection(stored_ids_set)
        return list(duplicate_ids)

    @staticmethod
    def get_filer_id(summaries, filing_id):
        row = list(filter(lambda x: x['filing_id'] == filing_id, summaries))
        return row[0]['filer_id'] if len(row) < 1 else ''
    # should this instead throw an exception?

    @staticmethod
    def is_id_valid(filer: str):
        return filer.isdigit()

    def get_updatable_filing_ids(self, summaries, ids):
        updatable_ids = []

        for id in ids:
            filer_id = self.get_filer_id(summaries, id)
            existing_filer_id = self.get_filer_id(self.summary_storage_list, id)
            if self.is_id_valid(existing_filer_id) or existing_filer_id == filer_id:
                continue # skip and do NOT update summaries with this id
            elif self.is_id_valid(filer_id):
                updatable_ids.append(id)

        return updatable_ids
    
    def get_new_filing_ids(self, summaries):
        ids_set = self.get_filing_ids_set(summaries)
        stored_ids_set = self.get_filing_ids_set(self.summary_storage_list)

        new_ids = ids_set.difference(stored_ids_set)
        return list(new_ids)
    
    @staticmethod
    def filter_summaries(summaries, ids):
        return list(filter(lambda x: x['filing_id'] in ids, summaries))

    def remove_summaries_in_storage(self, ids):
        self.summary_storage_list = list(
            filter(lambda x: x['filing_id'] not in ids, self.summary_storage_list))

   
    def add(self, summaries):
        new_ids = self.get_new_filing_ids(summaries)

        if len(new_ids) > 0:
            new_summaries = self.filter_summaries(summaries, new_ids)
            self.summary_storage_list += new_summaries

        duplicate_ids = self.get_duplicate_filing_ids(summaries)

        # conditionally update existing by checking each filing for a non 'filer_id' such as 'pending'
        if len(duplicate_ids) > 0:            
            ids_to_replace = self.get_updatable_filing_ids(summaries, duplicate_ids)
            self.remove_summaries_in_storage(ids_to_replace)

            # filter out ids_to_replace from _summary_storage_list then add the replacements
            if len(ids_to_replace) > 0:
                summaries_to_add = self.filter_summaries(summaries, ids_to_replace)
                self.summary_storage_list += summaries_to_add
