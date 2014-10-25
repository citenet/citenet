from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import pprint
from backend.crawler import Crawler

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/papers", methods = ['GET', 'POST'])
def get_papers():
    if request.form:
        paper_id = request.form['id']
    else:
        paper_id = "MED,23589462"
    crawler = Crawler()
    papers = crawler.crawl(paper_id, 10)
    return_dict = {id : paper.as_dict() for id, paper in papers.items()}
    return_list = [paper.as_dict() for id, paper in papers.items()]
    return jsonify(**{"list": return_list, "object": return_dict})

if __name__ == "__main__":
    app.run(debug=True)
