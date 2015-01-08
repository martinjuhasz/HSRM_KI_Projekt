from flask import Flask
from flask import render_template
from flask import request
from model.Result import Result
from Lucene.LuceneSearcher import LuceneSearcher
import math

app = Flask(__name__)

RESULTS_PER_PAGE = 10


@app.route('/', methods=['POST', 'GET'])
def search():

    # extract searchterm
    searchterm = None
    if request.args and request.args.get('q'):
        searchterm = request.args.get('q')

    current_page = 0
    if request.args and request.args.get('page'):
        current_page = int(request.args.get('page'))

    # extract results
    results = None
    duration = None
    count_results = None
    total_pages = 0
    if searchterm:
        # perform search
        searcher = LuceneSearcher()
        results_dic, duration, count_results = searcher.perform_search(searchterm, RESULTS_PER_PAGE, current_page)
        duration = duration.total_seconds()
        total_pages = int(math.ceil(count_results / RESULTS_PER_PAGE))
        results = []
        for res in results_dic:
            results.append(Result(res))

        """
        # add some dummy results
        results = []
        results.append(Result("Titel 1", "Lorem ipsum dolor", "https://placekitten.com/g/300/300"))
        results.append(Result("Titel 2", "Lorem ipsum dolor sit amet", "https://placekitten.com/g/550/550"))
        results.append(Result("Titel 3", "Lorem ipsum dolor lorem", "https://placekitten.com/g/500/500"))
        """



    return render_template('search.html', searchterm=searchterm, results=results, duration=duration, count_results=count_results, current_page=current_page, total_pages=total_pages)

if __name__ == "__main__":
    app.debug = True
    app.run()