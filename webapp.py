from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def main():
    dic = {"hello": "world"}
    return jsonify(**dic)

if __name__ == "__main__":
    app.run(debug=True)
