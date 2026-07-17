# matplotlib-slides

Minimal matplotlib wrapper for generating PDF slide decks. Every slide
automatically embeds a timestamp, git commit hash, and slide number.

## Usage

Write a plain script:

```python
# my_report.py
import numpy as np
from matplotlib_slides import Slides

with Slides("report.pdf", project_path="/path/to/repo") as deck:
    deck.title("My Report", subtitle="Sprint 42")

    with deck.one_plot("Signal") as ax:
        ax.plot(np.linspace(0, 6, 100), np.sin(np.linspace(0, 6, 100)))

    with deck.two_plots("Comparison") as (ax1, ax2):
        ax1.set_title("before"); ax2.set_title("after")

    with deck.four_plots("Overview") as (a, b, c, d):
        pass

    deck.text("Conclusions", body="• Point one\n• Point two")
```

Run it with uv — no installation needed:

```bash
uv run --with "matplotlib-slides @ git+https://github.com/benjaminhuth/matplotlib-slides" my_report.py
```

## Layouts

| Method | Axes |
|---|---|
| `deck.title(title, subtitle="")` | — |
| `with deck.one_plot(title="") as ax` | 1 |
| `with deck.two_plots(title="") as (ax1, ax2)` | 2 side-by-side |
| `with deck.four_plots(title="") as (a, b, c, d)` | 2×2 grid |
| `deck.text(title="", body="", fontsize=14)` | — |

## ROOT histogram plotting

`RootMpl1D` is a convenience wrapper for plotting 1-D ROOT histograms (`TH1`,
`TEfficiency`, `TProfile`) with matplotlib. It handles bin-edge centering,
asymmetric x-errors, and TEfficiency vs. TH1 fallback automatically.

```python
from matplotlib_slides import RootMpl1D

# TH1
h = RootMpl1D(th1_hist)
h.bar(ax, color="steelblue", alpha=0.7)
h.errorbar(ax, fmt="o", color="crimson")
h.step(ax, color="steelblue", lw=1.5)

# TEfficiency — automatically uses GetEfficiency / GetEfficiencyError*
e = RootMpl1D(efficiency_obj)
e.errorbar(ax, fmt="o", color="tomato")

# TProfile — uses GetBinContent / GetBinError
p = RootMpl1D(profile_obj)
p.bar(ax, color="seagreen", alpha=0.7)
p.errorbar(ax, fmt="o", color="darkgreen")
```

See [`examples/root_example.py`](examples/root_example.py) for a complete example
with synthetic TH1, TEfficiency, and TProfile objects (requires ROOT installed
separately).
