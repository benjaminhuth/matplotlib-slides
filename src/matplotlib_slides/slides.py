from contextlib import contextmanager
from pathlib import Path
import datetime
import subprocess

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


_FIGSIZE = (16, 9)
_MARGIN = 0.05
_FOOTER_H = 0.05
_HEADER_H = 0.10


def _git_query(project_path, *args):
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            cwd=project_path,
            timeout=5,
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "unknown"


class Slides:
    """Wraps matplotlib PdfPages to produce multi-slide PDF decks.

    Usage::

        with Slides("report.pdf", project_path="/path/to/repo") as deck:
            deck.title("My Report", subtitle="2024-01")
            with deck.one_plot("Timeseries") as ax:
                ax.plot(x, y)
            with deck.two_plots("Comparison") as (ax1, ax2):
                ax1.plot(...)
                ax2.bar(...)
            with deck.four_plots("Grid") as (ax1, ax2, ax3, ax4):
                ...
            deck.text("Conclusions", body="• Point one\\n• Point two")
    """

    def __init__(self, output_path, project_path, figsize=_FIGSIZE):
        self.output_path = Path(output_path)
        self.figsize = figsize
        self._pdf = None
        self._slide_number = 0
        self._timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self._repo = _git_query(project_path, "remote", "get-url", "origin")
        self._branch = _git_query(project_path, "rev-parse", "--abbrev-ref", "HEAD")
        self._commit = _git_query(project_path, "rev-parse", "--short", "HEAD")

    def __enter__(self):
        self._pdf = PdfPages(self.output_path)
        return self

    def __exit__(self, *args):
        self._pdf.close()

    # ------------------------------------------------------------------
    # internals

    def _new_fig(self):
        return plt.figure(figsize=self.figsize, facecolor="white")

    def _add_footer(self, fig):
        self._slide_number += 1
        label = (
            f"{self._timestamp}   |   {self._repo}   |   {self._branch}@{self._commit}"
            f"   |   slide {self._slide_number}"
        )
        fig.text(
            0.5,
            0.012,
            label,
            ha="center",
            va="bottom",
            fontsize=11,
            color="#999999",
            family="monospace",
        )

    def _finalize(self, fig):
        self._add_footer(fig)
        self._pdf.savefig(fig)
        plt.close(fig)

    def _content_rect(self, has_title):
        """Return (left, bottom, width, height) for the main content area."""
        top = 1.0 - ((_HEADER_H + _MARGIN) if has_title else _MARGIN)
        bottom = _FOOTER_H + _MARGIN
        left = _MARGIN
        width = 1.0 - 2 * _MARGIN
        height = top - bottom
        return left, bottom, width, height

    def _add_slide_title(self, fig, title):
        if title:
            fig.text(
                0.5,
                1.0 - _MARGIN / 2,
                title,
                ha="center",
                va="top",
                fontsize=22,
                fontweight="bold",
                color="#222222",
            )

    # ------------------------------------------------------------------
    # layouts

    def title(self, title, subtitle=""):
        """Full-page title slide — no axes yielded."""
        fig = self._new_fig()
        fig.text(
            0.5,
            0.56,
            title,
            ha="center",
            va="center",
            fontsize=44,
            fontweight="bold",
            color="#111111",
        )
        if subtitle:
            fig.text(
                0.5,
                0.44,
                subtitle,
                ha="center",
                va="center",
                fontsize=24,
                color="#555555",
            )
        self._finalize(fig)

    @contextmanager
    def one_plot(self, title=""):
        """Slide with a single axes."""
        fig = self._new_fig()
        self._add_slide_title(fig, title)
        l, b, w, h = self._content_rect(bool(title))
        ax = fig.add_axes([l, b, w, h])
        yield ax
        self._finalize(fig)

    @contextmanager
    def two_plots(self, title=""):
        """Slide with two side-by-side axes; yields (ax_left, ax_right)."""
        fig = self._new_fig()
        self._add_slide_title(fig, title)
        l, b, w, h = self._content_rect(bool(title))
        gap = _MARGIN
        half_w = (w - gap) / 2
        ax1 = fig.add_axes([l, b, half_w, h])
        ax2 = fig.add_axes([l + half_w + gap, b, half_w, h])
        yield ax1, ax2
        self._finalize(fig)

    @contextmanager
    def four_plots(self, title=""):
        """Slide with 2×2 axes grid; yields (top-left, top-right, bottom-left, bottom-right)."""
        fig = self._new_fig()
        self._add_slide_title(fig, title)
        l, b, w, h = self._content_rect(bool(title))
        gap = _MARGIN
        half_w = (w - gap) / 2
        half_h = (h - gap) / 2
        ax1 = fig.add_axes([l, b + half_h + gap, half_w, half_h])
        ax2 = fig.add_axes([l + half_w + gap, b + half_h + gap, half_w, half_h])
        ax3 = fig.add_axes([l, b, half_w, half_h])
        ax4 = fig.add_axes([l + half_w + gap, b, half_w, half_h])
        yield ax1, ax2, ax3, ax4
        self._finalize(fig)

    def text(self, title="", body="", fontsize=16):
        """Slide with a text body — no axes needed."""
        fig = self._new_fig()
        self._add_slide_title(fig, title)
        l, b, w, h = self._content_rect(bool(title))
        ax = fig.add_axes([l, b, w, h])
        ax.axis("off")
        if body:
            ax.text(
                0.0,
                1.0,
                body,
                ha="left",
                va="top",
                fontsize=fontsize,
                color="#222222",
                transform=ax.transAxes,
                linespacing=1.8,
            )
        self._finalize(fig)
