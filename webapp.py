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
    papers = crawler.crawl("MED,12634793", 40)
    returnDict = {id : paper.as_dict() for id, paper in papers.items()}
    print(returnDict)
    return jsonify(**returnDict)

if __name__ == "__main__":
    app.run(debug=True)
