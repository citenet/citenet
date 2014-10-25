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
    return_dict = {id : paper.as_dict() for id, paper in papers.items()}
    return_list = [paper.as_dict() for id, paper in papers.items()]
    return jsonify(**{"list": return_list, "object": return_dict})

if __name__ == "__main__":
    app.run(debug=True)
