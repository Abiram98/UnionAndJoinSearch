class Search:
    def __init__(self, inv_index, cat_index, table_dir):
        self.__inv_index = inv_index
        self.__cat_index = cat_index
        self.__table_dir = table_dir

    def get_inv_index(self):
        return self.__inv_index

    def get_category_index(self):
        return self.__cat_index

    def get_table_dir(self):
        return self.__table_dir

    def search(self, query):
        raise Exception('search is not implemented')

    def filter_corpus(self, types):
        tables = set()

        for type in types:
            if type in self.__inv_index.keys():
                tables = tables.union(self.__inv_index[type])

        return tables

    def jaccard(self, s1, s2):
        return float(len(s1.intersection(s2))) / float(len(s1.union(s2)))
