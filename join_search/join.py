import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from search import Search

class Join(Search):
    def __init__(self, index, cat_index, table_dir):
        super().__init__(index, cat_index, table_dir)

    def joinability(self, q_column_categories, t_column_categories):
        max_score = 0
        best_q_column = -1
        best_t_column = -1

        for q in range(len(q_column_categories)):
            for t in range(len(t_column_categories)):
                jacc = super().jaccard(q_column_categories[q], t_column_categories[t])

                if jacc > max_score:
                    max_score = jacc
                    best_q_column = q
                    best_t_column = t

        return max_score

    def search(self, query):
        q_column_categories = list()
        all_categories = set()
        progress = 0

        # Collect all types per column
        for j in range(len(query[0])):
            tmp_column_categories = set()

            for i in range(len(query)):
                entity = query[i][j]
                categories = super().get_category_index()[entity]
                all_categories = all_categories.union(categories)
                tmp_column_categories = tmp_column_categories.union(categories)

            q_column_categories.append(tmp_column_categories)

        # Prefilter corpus based on categories
        corpus = super().filter_corpus(all_categories)
        results = list()

        # Score tables according to they joinability
        for table in corpus:
            print(' ' * 100, end = '\r')
            print('Progress: ' + str((progress / len(corpus)) * 100)[:5] + '%', end = '\r')
            progress += 1

            with open(super().get_table_dir() + '/' + table, 'r') as handle:
                table_obj = json.load(handle)['rows']
                t_column_categories = list()

                for j in range(len(table_obj[0])):
                    tmp_column_categories = set()

                    for i in range(len(table_obj)):
                        cell = table_obj[i][j]

                        if 'categories' in cell.keys():
                            tmp_column_categories = tmp_column_categories.union(cell['categories'])

                    t_column_categories.append(tmp_column_categories)

                score = self.joinability(q_column_categories, t_column_categories)

                if score > 0.0:
                    results.append((table, score))

        results.sort(reverse = True, key = lambda result: result[1])
        return results
