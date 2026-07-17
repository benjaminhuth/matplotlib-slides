import numpy as np


class RootMpl1D:
    def __init__(self, root_hist, skip_empty_bins=False):
        try:
            th1 = root_hist.GetTotalHistogram()
        except AttributeError:
            th1 = root_hist

        bins = list(range(1, th1.GetNbinsX() + 1))
        if skip_empty_bins:
            bins = [i for i in bins if th1.GetBinContent(i) > 0.0]

        self.x = [th1.GetBinCenter(i) for i in bins]

        self.x_lo = [th1.GetBinLowEdge(i) for i in bins]
        self.x_width = [th1.GetBinWidth(i) for i in bins]
        self.x_hi = np.add(self.x_lo, self.x_width)
        self.x_err_lo = np.subtract(self.x, self.x_lo)
        self.x_err_hi = np.subtract(self.x_hi, self.x)
        self.edges = list(self.x_lo) + [self.x_hi[-1]]

        try:
            self.y = [root_hist.GetEfficiency(i) for i in bins]
            self.y_err_lo = [root_hist.GetEfficiencyErrorLow(i) for i in bins]
            self.y_err_hi = [root_hist.GetEfficiencyErrorUp(i) for i in bins]
        except AttributeError:
            self.y = [root_hist.GetBinContent(i) for i in bins]
            self.y_err_lo = [root_hist.GetBinError(i) for i in bins]
            self.y_err_hi = [root_hist.GetBinError(i) for i in bins]

    def errorbar(self, ax, **errorbar_kwargs):
        ax.errorbar(
            self.x,
            self.y,
            yerr=(self.y_err_lo, self.y_err_hi),
            xerr=(self.x_err_lo, self.x_err_hi),
            **errorbar_kwargs,
        )
        return ax

    def stairs(self, ax, **stairs_kwargs):
        stairs_kwargs.setdefault("fill", False)
        ax.stairs(self.y, self.edges, **stairs_kwargs)
        return ax

    def bar(self, ax, **bar_kwargs):
        bar_kwargs.setdefault("width", self.x_width)
        ax.bar(self.x, height=self.y, yerr=(self.y_err_lo, self.y_err_hi), **bar_kwargs)
        return ax
