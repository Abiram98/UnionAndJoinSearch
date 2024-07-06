import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from search import Search
import json
import numpy as np
from scipy.optimize import linear_sum_assignment

class Union(Search):
    def __init__(self, inv_index, cat_index, table_dir):
        super().__init__(inv_index, cat_index, table_dir)

    def aggregate_scores(self, q_column_categories, t_column_categories):
        matrix = list()

        for i in range(len(q_column_categories)):
            row = list()

            for j in range(len(t_column_categories)):
                jacc = super().jaccard(q_column_categories[i], t_column_categories[j])
                row.append(jacc)

            matrix.append(row)

        matrix = np.array(matrix)
        row_indices, column_indices = linear_sum_assignment(matrix)

        return matrix[row_indices, column_indices].sum() / len(q_column_categories)

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

        # Pre-filter corpus to only contain tables containing types included in the query
        corpus = super().filter_corpus(all_categories)
        results = list()

        # Score tables according to their unionability
        for table in corpus:
            print(' ' * 100, end = '\r')
            print('Progress: ' + str((progress / len(corpus)) * 100)[:5] + '%', end = '\r')
            progress += 1

            with open(super().get_table_dir() + '/' + table, 'r') as handle:
                table_obj = json.load(handle)['rows']
                t_column_categories = list()

                if len(table_obj[0]) != len(query[0]):
                    continue

                for j in range(len(table_obj[0])):
                    tmp_column_categories = set()

                    for i in range(len(table_obj)):
                        cell = table_obj[i][j]

                        if 'categories' in cell.keys():
                            tmp_column_categories = tmp_column_categories.union(cell['categories'])

                    t_column_categories.append(tmp_column_categories)

                score = self.aggregate_scores(q_column_categories, t_column_categories)

                if score > 0.0:
                    results.append((table, score))

        results.sort(reverse = True, key = lambda result: result[1])
        return results
