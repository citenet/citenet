from flask import Flask
from flask import render_template
from flask import jsonify
import pprint
from backend.crawler import Crawler

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/papers")
def get_papers():
    crawler = Crawler()
    papers = crawler.crawl("MED,23589462", 10)
    returnDict = {id : paper.as_dict() for id, paper in papers.items()}
    returnList = [paper.as_dict() for id, paper in papers.items()]
    return jsonify(**{"list": returnList, "object":     returnDict})

if __name__ == "__main__":
    app.run(debug=True)
