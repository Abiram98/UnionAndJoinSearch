import os
import json
import sys
import pickle
from union_search.union import Union
from join_search.join import Join
import measure_performance as mp

if __name__=="__main__":
    k = 10
    tuples = -1
    query_dir = sys.argv[1]
    index_path = sys.argv[2]
    cat_index_path = sys.argv[3]
    corpus_dir = sys.argv[4]
    result_dir = sys.argv[5]
    search = Union
    index = None
    cat_index = None
    queries = list()
    query_count = 1
    query_files = os.listdir(query_dir)

    with open(index_path, 'rb') as handle:
        index = pickle.load(handle)

    with open(cat_index_path) as handle:
        cat_index = json.load(handle)

    if sys.argv[6] == 'union':
        search = Union(index, cat_index, corpus_dir)

    elif sys.argv[6] == 'join':
        search = Join(index, cat_index, corpus_dir)

    else:
        print('Did not understand search type')
        exit(1)

    with open(query_dir + '/' + query_files[0], 'r') as handle:
        tuples = len(json.load(handle)['queries'])

    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

        for query_file in query_files:
            print('\nQuery ' + str(query_count))
            query_count += 1

            with open(query_dir + '/' + query_file, 'r') as handle:
                obj = json.load(handle)
                query = obj['queries']
                results = search.search(query)

                with open(result_dir + query_file, 'w') as result_handle:
                    json.dump({'results': results}, result_handle)

    if tuples == -1:
        raise Exception('No queries evaluated, so scores cannot be computed')

    scores = mp.ndcg(result_dir, k, tuples)
    print('NDCG')

    for query in scores.keys():
        print(scores[query]['ndcg'])

    print('\nPrecision')

    for query in scores.keys():
        print(scores[query]['precision'])

    print('\nRecall')

    for query in scores.keys():
        print(scores[query]['recall'])

    print('\nF1-score')

    for query in scores.keys():
        print(scores[query]['f1'])
