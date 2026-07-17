# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "matplotlib-slides @ git+https://github.com/benjaminhuth/matplotlib-slides",
#   "numpy",
# ]
# ///
#
# Run from a local checkout:
#   uv run python examples/root_example.py
#
# Run directly from GitHub (no local checkout needed):
#   uv run https://raw.githubusercontent.com/benjaminhuth/matplotlib-slides/main/examples/root_example.py
#
# NOTE: Requires ROOT to be installed separately (not pip-installable).

import numpy as np
from matplotlib_slides import Slides, RootMpl1D


def main():
    import ROOT

    rng = np.random.default_rng(42)

    # --- TH1F: Gaussian ---
    th1 = ROOT.TH1F("h", "h", 50, -3, 3)
    for _ in range(10000):
        th1.Fill(rng.normal(0, 1))

    # --- TEfficiency: sigmoid efficiency curve ---
    eff = ROOT.TEfficiency("e", "e", 20, -3, 3)
    for x in rng.normal(0, 1, 5000):
        passed = rng.uniform() < 0.3 + 0.5 / (1 + np.exp(-x))
        eff.Fill(int(passed), x)

    # --- TProfile: linear trend with noise ---
    prof = ROOT.TProfile("p", "p", 20, -3, 3, 0, 5)
    for x in rng.normal(0, 1, 5000):
        prof.Fill(x, 2 + 0.5 * x + rng.normal(0, 0.3))

    with Slides("root_example.pdf", project_path=".") as deck:

        deck.title(
            "ROOT 1-D histograms in matplotlib",
            subtitle="RootMpl1D · TH1 · TEfficiency · TProfile",
        )

        with deck.one_plot("TH1 — bar + errorbar") as ax:
            h = RootMpl1D(th1)
            h.bar(ax, color="steelblue", alpha=0.7, label="bar")
            h.errorbar(ax, fmt="o", color="crimson", ms=3, label="errorbar")
            ax.legend()
            ax.set_xlabel("x [a.u.]")
            ax.set_ylabel("counts")

        with deck.one_plot("TH1 — stairs") as ax:
            h = RootMpl1D(th1)
            h.stairs(ax, color="steelblue", lw=1.5, label="stairs")
            ax.legend()
            ax.set_xlabel("x [a.u.]")
            ax.set_ylabel("counts")

        with deck.one_plot("Efficiency") as ax:
            e = RootMpl1D(eff)
            e.errorbar(ax, fmt="o", color="tomato", label="efficiency")
            ax.set_ylim(0, 1)
            ax.legend()
            ax.set_xlabel("x [a.u.]")
            ax.set_ylabel("efficiency")

        with deck.one_plot("TProfile — bar + errorbar") as ax:
            p = RootMpl1D(prof)
            p.bar(ax, color="seagreen", alpha=0.7, label="profile")
            p.errorbar(ax, fmt="o", color="darkgreen", ms=3, label="errorbar")
            ax.legend()
            ax.set_xlabel("x [a.u.]")
            ax.set_ylabel("<y>")

    print("Wrote root_example.pdf")


if __name__ == "__main__":
    main()
