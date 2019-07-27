from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

ROW_IDS = ["A", "B", "C"]
ANSWER_RANGE_MIN = 1
ANSWER_RANGE_MAX = 7


@app.route("/")
def table_form():
    return render_template("table_form.html", row_ids=ROW_IDS)


@app.route("/plot", methods=["post"])
def make_plot():
    print(request)
    result_array = np.zeros(shape=(len(ROW_IDS), len(ROW_IDS)))
    for i, col_id in enumerate(ROW_IDS):
        for j, row_id in enumerate(ROW_IDS):
            result_array[i, j] = int(
                request.form[f"doti_{col_id}_{row_id}"] or "0"
            )
    print(result_array)
    return "ok"
