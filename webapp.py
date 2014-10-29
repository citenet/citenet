from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import pprint
from backend.crawler import Crawler

import os # to get env variables for heroku

import time

app = Flask(__name__, static_url_path='')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/papers", methods = ['GET', 'POST'])
def get_papers():
    start = time.time()

    if request.form:
        paper_id = request.form['id']
    else:
        paper_id = "MED,23589462"

    crawler = Crawler()
    tree = crawler.crawl(paper_id, 3)

    end = time.time()
    print end - start

    return jsonify(**{"list": tree.as_list(), "object": tree.as_dict()})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000)) # use port variable or 5000
    app.run(debug=True, port=port)
