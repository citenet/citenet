from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import pprint
from backend.crawler import Crawler

import time

app = Flask(__name__)

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
    papers = crawler.crawl(paper_id, 10)
    return_dict = {id: paper.as_dict() for id, paper in papers.items()}
    return_list = [paper.as_dict() for id, paper in papers.items()]

    end = time.time()
    print end - start

    return jsonify(**{"list": return_list, "object": return_dict})

if __name__ == "__main__":
    app.run(debug=True)
