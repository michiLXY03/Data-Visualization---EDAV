import json
from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask(__name__, 
            static_url_path='',
            static_folder='static',
            template_folder='templates')

COL_CARE = ["loan_amnt", "loan_status", "zip_code", "annual_inc", "term", "int_rate",
            "grade", "purpose", "issue_d", "addr_state"]

TIME_DATA_CACHE = None
STATS_DATA_CACHE = None
GEO_DATA_CACHE = None
PURP_DATA_CACHE = None

@app.route("/loading")
def loading():
    return render_template("loading.html")

@app.route("/stats")
def bystats():
    jsonify_data = json.dumps(STATS_DATA_CACHE, indent=2)
    jsonify_data_purp = json.dumps(PURP_DATA_CACHE, indent=2)
    return render_template("stats.html", stats_data=jsonify_data, purp_data=jsonify_data_purp)

@app.route("/timeseries")
def bytime():
    jsonify_data = json.dumps(TIME_DATA_CACHE, indent=2)
    return render_template("time.html", time_data=jsonify_data)

@app.route("/geomap")
def bygeo():
    jsonify_data = json.dumps(GEO_DATA_CACHE, indent=2)
    return render_template("geomap.html", data=jsonify_data)

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

def load_data():
    import time
    s = time.time()
    global TIME_DATA_CACHE
    global STATS_DATA_CACHE
    global GEO_DATA_CACHE
    global PURP_DATA_CACHE
    
    STATS_DATA_CACHE = pd.read_csv("stats_data.csv").to_dict("records")
    TIME_DATA_CACHE = pd.read_csv("time_data.csv").to_dict("records")
    GEO_DATA_CACHE = pd.read_csv("geo_date.csv").to_dict("records")
    PURP_DATA_CACHE = pd.read_csv("stats_purpose_data.csv").to_dict("records")

    print(time.time() - s)

@app.before_first_request
def loading_data():
    from threading import Thread
    loadint_tr = Thread(target=load_data)
    loadint_tr.start()

if __name__ == "__main__":
    app.run(debug=True)
