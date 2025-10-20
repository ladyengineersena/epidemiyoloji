from __future__ import annotations

from typing import Dict

import matplotlib.pyplot as plt
import numpy as np


def plot_compartments(results: Dict[str, np.ndarray], title: str | None = None):
    t = results["t"]
    S = results["S"]
    E = results["E"]
    I = results["I"]
    R = results["R"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t, S, label="S (Susceptible)", linewidth=2)
    ax.plot(t, E, label="E (Exposed)", linewidth=2)
    ax.plot(t, I, label="I (Infectious)", linewidth=2)
    ax.plot(t, R, label="R (Recovered)", linewidth=2)

    ax.set_xlabel("Days", fontsize=12)
    ax.set_ylabel("Population", fontsize=12)
    if title:
        ax.set_title(title, fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)
    fig.tight_layout()
    return fig, ax
