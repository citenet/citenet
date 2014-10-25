from flask import Flask
from flask import render_template
from flask import jsonify
from backend.crawler import Crawler

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/papers")
def get_papers():
    crawler = Crawler()
    papers = crawler.crawl("10.1038/nature01511", 5)
    print papers
    return jsonify(**papers)

if __name__ == "__main__":
    app.run(debug=True)
