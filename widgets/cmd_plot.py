"""C3 — Kümülatif Kütle Dağılımı (CMD) ve %50 → MMAD kesişimi.

İki eğri:
  - Kümülatif undersize (%) vs aerodinamik çap (log eksen)
  - %50 yatay çizgisi ve MMAD'ye düşen dikey kesişim (d50 okuması)
Eğitim amacı: kullanıcı MMAD/GSD oynattıkça eğrinin nasıl kaydığını ve
%50 kesişimin doğrudan MMAD verdiğini görür.
"""

import numpy as np

from widgets.mpl_canvas import ACCENT, ACCENT_DARK, GRID, INK, MUTED, WARN, MplCanvas
from core.models import _lognorm_dist


class CMDChart(MplCanvas):
    def __init__(self):
        super().__init__(width=5.4, height=3.6)

    def update_plot(self, mmad, gsd, total_dose=1000.0):
        self.clear()

        # Düzgün log-aralıklı çap ekseni
        d = np.logspace(np.log10(0.1), np.log10(30.0), 240)
        cdf = _lognorm_dist(mmad, gsd).cdf(d) * 100.0

        self.ax.plot(d, cdf, color=ACCENT, linewidth=2.2, zorder=3)
        self.ax.set_xscale("log")
        self.ax.set_xlim(0.1, 30)
        self.ax.set_ylim(0, 100)
        self.ax.set_xlabel("Aerodinamik çap (µm, log)")
        self.ax.set_ylabel("Kümülatif undersize (%)")
        self.ax.set_title("Kümülatif Kütle Dağılımı (CMD)",
                          fontsize=10, loc="left")

        # %50 yatay + MMAD dikey kesişim
        self.ax.axhline(50, color=MUTED, linewidth=0.9,
                        linestyle="--", zorder=2)
        self.ax.axvline(mmad, color=WARN, linewidth=1.4,
                        linestyle="--", zorder=2)
        self.ax.plot([mmad], [50], "o", color=WARN, markersize=7, zorder=4)
        self.ax.annotate(
            f"MMAD = {mmad:.1f} µm  (d₅₀)",
            xy=(mmad, 50), xytext=(8, -18),
            textcoords="offset points", fontsize=8.5,
            color=WARN, fontweight="bold",
        )

        # d16 / d84 referans noktaları (GSD görselleştirme)
        dist = _lognorm_dist(mmad, gsd)
        d16 = float(dist.ppf(0.1587))
        d84 = float(dist.ppf(0.8413))
        for dx, pct, lbl in ((d16, 15.87, "d₁₆"), (d84, 84.13, "d₈₄")):
            self.ax.plot([dx], [pct], "o", color=ACCENT_DARK,
                         markersize=4.5, zorder=4)
            self.ax.annotate(lbl, xy=(dx, pct), xytext=(4, 2),
                             textcoords="offset points",
                             fontsize=7.5, color=ACCENT_DARK)

        self.ax.grid(True, which="both", color=GRID, linewidth=0.5)
        self.ax.set_axisbelow(True)
        self.fig.text(
            0.5, 0.01,
            f"GSD = {gsd:.2f}  →  d₈₄/d₅₀ = {d84/mmad:.2f}  (log-normal teyidi)",
            ha="center", fontsize=7.5, color=MUTED,
        )
        self.fig.tight_layout(rect=(0, 0.04, 1, 1))
        self.draw()
