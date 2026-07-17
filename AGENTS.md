# matplotlib-slides — agent instructions

## What this is

Single-class library (`Slides`) wrapping `matplotlib.backends.backend_pdf.PdfPages`
to produce PDF slide decks.  Exported as `matplotlib_slides.Slides`.
No CLI entrypoint — write a plain Python script.

## Key structure

| Path | Role |
|---|---|
| `src/matplotlib_slides/__init__.py` | Exports `Slides` and `RootMpl1D` |
| `src/matplotlib_slides/slides.py` | ~200 lines — slide deck logic |
| `src/matplotlib_slides/root_mpl_hist1d.py` | ROOT→matplotlib 1-D bridge (`RootMpl1D` class) |
| `examples/example.py` | General example (no ROOT); has inline uv script header |
| `examples/root_example.py` | ROOT-specific example (TH1, TEfficiency, TProfile) |
| `pyproject.toml` | hatchling build, src-layout, deps: `matplotlib>=3.5`, `numpy>=1.21` |

## Commands

```bash
# run the example (local checkout)
uv run python examples/example.py
uv run python examples/root_example.py        # requires ROOT installed

# run the example directly from GitHub (no checkout)
uv run https://raw.githubusercontent.com/benjaminhuth/matplotlib-slides/main/examples/example.py
uv run https://raw.githubusercontent.com/benjaminhuth/matplotlib-slides/main/examples/root_example.py

# install in editable mode
uv pip install -e .

# format (only tool: Black via pre-commit)
pre-commit run --all-files
```

## Important quirks

- **`project_path` is required.** `Slides(..., project_path=".")` — runs `git rev-parse` in that directory for the footer metadata. Pass the repo root.
- **No tests, no CI, no type checker, no linter.** Black via pre-commit is the only formatting. Do not invent a test harness or CI workflow without asking.
- **Context manager pattern** — all plot slides (`one_plot`, `two_plots`, `four_plots`) are context managers that yield axes; the user plots inside `with` blocks. `title()` and `text()` are plain methods (no yield).
- **Footer is automatic** — every slide embeds: timestamp · git remote · branch@commit · slide number.
- **`root_mpl_hist1d.py`** provides `RootMpl1D`, exported from `__init__.py`. Experimental.
- **Permissions.** `.claude/settings.local.json` allows `uv run *`, the example script, and `xdg-open` for PDF viewing.
