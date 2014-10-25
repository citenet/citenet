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
    return_dict = {id: paper.as_dict() for id, paper in papers.items()}
    return_list = [paper.as_dict() for id, paper in papers.items()]
    with open('graph.dot', 'w') as the_file:
        print >> the_file, "digraph citations {"
        print >> the_file, "splines=true;"
        print >> the_file, 'sep="+25,25";'
        print >> the_file, "overlap=scalexy;"
        print >> the_file, "node [fontsize=11];"
        for _, paper in papers.items():
            for ref in paper.references:
                print >> the_file, "%s -> %s" % ('"%s %s%s"' % (paper.api_id.replace('MED,',''), str(paper.walked)[0], str(paper.has_references)[0]), '"%s %s%s"' % (ref.replace('MED,',''), str(papers[ref].walked)[0], str(papers[ref].has_references)[0]))
                #print "%s -> %s" % (paper.api_id.replace('MED,','') + paper.date, ref.replace('MED,','') + papers[ref].date)
        print >> the_file, "}"
    return jsonify(**{"list": return_list, "object": return_dict})

if __name__ == "__main__":
    app.run(debug=True)
