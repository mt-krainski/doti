import base64
import io
import json
from string import ascii_uppercase
from textwrap import wrap

from flask import Flask, render_template, request, Response
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from doti import plot

app = Flask(__name__)

ANSWER_RANGE_MIN = 1
ANSWER_RANGE_MAX = 7


@app.route("/")
def table_form():
    entries = int(request.args.get("entries", 3))
    return render_template(
        "table_form.html", row_ids=ascii_uppercase[:entries], entries=entries
    )


@app.route("/plot", methods=["post"])
def make_plot():
    form = request.json
    entries = int(form["entries"])
    entry_ids = ascii_uppercase[:entries]
    result_array = np.zeros(shape=(entries, entries))
    for i, col_id in enumerate(entry_ids):
        for j, row_id in enumerate(entry_ids):
            if form[f"doti_{col_id}_{row_id}"] == "":
                result_array[i, j] = None
                continue
            try:
                result_array[i, j] = int(form[f"doti_{col_id}_{row_id}"])
            except ValueError:
                result_array[i, j] = None

    title = form["doti_title"]
    title = "\n".join(wrap(title, 60))
    if form["doti_subtitle"]:
        title += f"\n{form['doti_subtitle']}"

    fig = plot(
        result_array,
        plot_title=title + "\n",
        cmap="Reds_r",
        vmin=ANSWER_RANGE_MIN - 0.5,
        vmax=ANSWER_RANGE_MAX + 0.5,
    )

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(base64.b64encode(output.getvalue()), mimetype="image/png")
