from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def search():
    print request.args
    print request.form

    return render_template('search.html')

if __name__ == "__main__":
    app.debug = True
    app.run()