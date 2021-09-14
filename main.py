from flask import Flask, render_template, request, jsonify

from googlevs import get_d3_json
import os
import json


app = Flask(__name__)

@app.route("/")
def main():
    seed = request.args.get('seed', 'bloom filter')
    seed = seed.lower()
    fp = os.getcwd() + "/static/" + seed + ".json"

    if not seed or os.path.isfile(fp):
        print("no seed")
        return render_template("home.html", seed=seed)
    else:
        js = get_d3_json(seed)
        with open(fp, "w") as f:
            f.write(json.dumps(js))
        return render_template("home.html", seed=seed)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/data")
def data():
    seed = request.args.get('seed')
    js = get_d3_json(seed)
    return jsonify(js)


if __name__ == "__main__":
    print("Running")
    app.run("0.0.0.0", debug=True)