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
