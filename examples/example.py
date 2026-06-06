# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "matplotlib-slides @ git+https://github.com/benjaminhuth/matplotlib-slides",
#   "numpy",
# ]
# ///
#
# Run directly from GitHub (no local checkout needed):
#   uv run https://raw.githubusercontent.com/benjaminhuth/matplotlib-slides/main/examples/example.py
#
# Run from a local checkout:
#   uv run python examples/example.py

import numpy as np
from matplotlib_slides import Slides


def main():
    rng = np.random.default_rng(42)
    x = np.linspace(0, 2 * np.pi, 200)

    with Slides("example_slides.pdf", project_path=".") as deck:

        deck.title("matplotlib-slides", subtitle="Example deck · all five layouts")

        with deck.one_plot("Sine & cosine") as ax:
            ax.plot(x, np.sin(x), label="sin(x)")
            ax.plot(x, np.cos(x), label="cos(x)", linestyle="--")
            ax.set_xlabel("x")
            ax.legend()
            ax.grid(alpha=0.3)

        with deck.two_plots("Signal vs. noise") as (ax1, ax2):
            ax1.plot(x, np.sin(x), color="steelblue")
            ax1.set_title("Clean signal")
            ax1.grid(alpha=0.3)

            noisy = np.sin(x) + rng.normal(0, 0.4, len(x))
            ax2.plot(x, noisy, color="tomato", linewidth=0.8)
            ax2.set_title("Noisy signal")
            ax2.grid(alpha=0.3)

        with deck.four_plots("Histogram gallery") as (ax1, ax2, ax3, ax4):
            for ax, color, label in zip(
                (ax1, ax2, ax3, ax4),
                ("steelblue", "tomato", "seagreen", "darkorange"),
                ("uniform", "normal", "exponential", "beta"),
            ):
                samples = {
                    "uniform": rng.uniform(0, 1, 120),
                    "normal": rng.normal(0, 1, 120),
                    "exponential": rng.exponential(1, 120),
                    "beta": rng.beta(2, 5, 120),
                }[label]
                ax.hist(samples, bins=20, color=color, alpha=0.8)
                ax.set_title(label)

        deck.text(
            title="How to use",
            body=(
                "from matplotlib_slides import Slides\n\n"
                "with Slides('report.pdf', project_path='/path/to/repo') as deck:  # repo/branch/commit auto-detected\n"
                "    deck.title('Title', subtitle='...')\n"
                "    with deck.one_plot('My plot') as ax:\n"
                "        ax.plot(x, y)\n"
                "    with deck.two_plots('Side by side') as (ax1, ax2):\n"
                "        ax1.plot(...)\n"
                "    with deck.four_plots('Grid') as (a, b, c, d):\n"
                "        ...\n"
                "    deck.text('Notes', body='• bullet\\n• bullet')\n\n"
                "Every slide embeds: timestamp · repo · branch@commit · slide number."
            ),
            fontsize=12,
        )

    print("Wrote example_slides.pdf")


if __name__ == "__main__":
    main()
