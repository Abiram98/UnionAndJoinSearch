# Evaluation of Union and Join Search for Semantic Data Discovery
We will implement two simplistic approaches for Wiki union and join search.
We will evaluate these two approaches on a benchmark for semantic data discovery of Wikipedia tables ("<a href="https://github.com/dkw-aau/SemanticTableSearchDataset1~https://github.com/dkw-aau/SemanticTableSearchDataset">A Large Scale Test Corpus for Semantic Table Search</a>") containing automatically constructed ground truth using Wikipedia cateogories.

## Union search
We implement a naive baseline for union search using Wikipedia annotations for similarity union search.
Given an input table, we find unionable tables based on column-centric similarity, i.e., we use a similarity function over table columns to compute an aggregated unionability score per table.
Specifically, we annotate entity cells with their correspoding Wikipedia page categories and represent the table column as the collection of Wikipedia categories of its entity cells.
Then, we measure the Jaccard similarity between pairs of columns between the input table and candidate table.
We apply the Hungarian algorithm to find the best combination of column pairs to maximize the aggregated table score.

## Join Search
We once again implement a naive baseline for join search using Wikipedia annotations for similarity join search.
The aim is to find tables that contains a joinable column with a query column based on overlap of Wikipedia categories of Wikipedia entities in table cells.
This overlap is once again measured with the Jaccard similarity.

For each query-table pair, we find the best pair of columns between the query table and the candidate table that maximize the Jaccard similarity.
This maximum score represents the table score and is used in the final ranking of the tables.

## Experimental Evaluation

### Setup
We evaluate the two baselines against a semanic table search corpus constructed based on Wikipedia tables ("<a href="https://github.com/dkw-aau/SemanticTableSearchDataset1~https://github.com/dkw-aau/SemanticTableSearchDataset">A Large Scale Test Corpus for Semantic Table Search</a>").
We randomly select 12 queries from the corpus tables, and ground truth is automatically extracted through distant supervision.
The table queries consist of DBpedia entities, which we substitute with their corresponding Wikipedia entity through the RDF "isPrimaryTopicOf" relations.
This allows us to annotate the query entities with their corresponding Wikipedia categories.

### Results
We now present the experimental result of the union and join search approaches.
We evaluate union and join search using NDCG and recall for top-10 ranking and retrieval of tables.
NDCG evalutes the ranking of tables, whereas the remaining evaluate the effectiveness of table retrieval.

The ranking performance is varying, where some queries effectively ranks tables according ot ground truth and therefore achive a perfect performance score, whereas other queries are not able to retrieve and rank any tables at all.
It should be notes that the Wikipedia categories per Wikipedia entity are sparse and very specific.
For example, <a href="https://en.wikipedia.org/wiki/South_Korea_at_the_2010_Asian_Games">South Korea at the 2010 Asian Games</a> has the specific categories <a href="https://en.wikipedia.org/wiki/Category:2010_in_South_Korean_sport">2010 in South Korean sport</a>, <a href="https://en.wikipedia.org/wiki/Category:South_Korea_at_the_Asian_Games1">South Korea at the Asian Games</a>, and <a href="https://en.wikipedia.org/wiki/Category:Nations_at_the_2010_Asian_Games>Nations at the 2010 Asian Games</a>.
Due to the very specific and generally low number of categories, the Jaccard similarity tends to often be very low when comparing columns of tables.
Therefore, as an example, a query table might have a column category which is the only category shared in a candidate table.

The results presenting recall indicate the same weakness of the implemented approaches.
The approaches assign low unionability and joinability scores due to the limitations of the Wikipedia categories.
This makes the approaches ineffective in correctly ranking the candidate tables.
Therefore, many of the top-10 highest ranking ground truth relevant tables are not included in the result set of the approaches.

A surprising result is that both union and join search achieve the same performance.
Union search is more restricted, as it aims to vertically extend the query table and therefore require the set of columns of the candidate tables to match the set of query table columns.
For join search, this requirement is relaxed, as it aims horizontally extend the query tables and do not have any row-level schema requirements.
Join search simply must rank tables based on highest overlap of Wikipedia categories for a single query column against a single candidate table column.
This leads one to question what would be the performance of union search if its column restriction is removed.

#### Conclusion
The lack of information per Wikipedia entity poses a limitation in the accuracy of implemented, naive approaches, as well as their ability to rank tables.
However, given the results measured with NDCG, the naive approaches for union and join search are still able to retrieve some relevant tables and can therefore indeed be used as table discovery approaches.
