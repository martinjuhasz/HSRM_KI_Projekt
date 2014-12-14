from flask import Flask
from flask import render_template
from flask import request
from model.Result import Result
from Lucene.LuceneSearcher import LuceneSearcher

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def search():

    # extract searchterm
    searchterm = None
    if request.form and request.form["searchterm"]:
        searchterm = request.form["searchterm"]

    # extract results
    results = None
    if searchterm:
        # perform search
        searcher = LuceneSearcher()
        results_dic, duration = searcher.perform_search(searchterm)

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

    return render_template('search.html', searchterm=searchterm, results=results)

if __name__ == "__main__":
    app.debug = True
    app.run()