import shutil
from textwrap import wrap
from typing import Union

from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import string


def plot(dataset: np.ndarray, plot_title: Union[str, None] = None, **kwargs):

    dataset = dataset
    x = list(range(dataset.shape[1]))
    y = list(range(0, -dataset.shape[0], -1))

    xx, yy = np.meshgrid(x, y)
    xx = xx.flatten()
    yy = yy.flatten()

    fig, ax = plt.subplots()

    im = ax.scatter(
        xx, yy, s=200 * (8 - dataset[-yy, xx]), c=dataset[-yy, xx], **kwargs
    )

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    plt.colorbar(im, cax=cax)
    ax.axis("equal")
    ax.xaxis.tick_top()
    ax.set_xticks(x, minor=False)
    ax.set_yticks(y, minor=False)
    ax.set_xticklabels(
        list(string.ascii_uppercase)[: dataset.shape[1]], minor=False
    )
    ax.set_yticklabels(
        list(string.ascii_uppercase)[: dataset.shape[0]], minor=False
    )
    ax.set_xlim([min(x) - 0.75, max(x) + 0.75])
    ax.set_ylim([min(y) - 0.75, max(y) + 0.75])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    if plot_title is not None:
        ax.set_title(plot_title, pad=20)

    plt.tight_layout()
    return fig
