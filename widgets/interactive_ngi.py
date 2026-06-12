"""C1 — NGI kademe deposizyon bar grafiği (canlı)."""

from widgets.mpl_canvas import ACCENT, ACCENT_DARK, GRID, MUTED, MplCanvas
from core.models import compute_apsd


class NGIChart(MplCanvas):
    def __init__(self):
        super().__init__(width=5.4, height=3.6)

    def update_plot(self, mmad, gsd, total_dose=1000.0):
        r = compute_apsd(mmad, gsd, total_dose)
        self.clear()
        stages = list(r.stage_fractions.keys())
        vals = list(r.stage_fractions.values())
        # En yüksek kademeyi vurgula
        peak = vals.index(max(vals))
        colors = [ACCENT_DARK if i == peak else ACCENT for i in range(len(vals))]
        bars = self.ax.bar(stages, vals, color=colors, width=0.66)
        self.ax.set_ylabel("Kütle fraksiyonu (%)")
        self.ax.set_title("NGI Kademe Deposizyon Profili", fontsize=10, loc="left")
        self.ax.set_ylim(0, max(vals) * 1.25 + 1)
        for b, v in zip(bars, vals):
            if v >= 1.0:
                self.ax.text(b.get_x() + b.get_width() / 2, v + 0.3,
                             f"{v:.0f}", ha="center", va="bottom",
                             fontsize=7, color=MUTED)
        self.ax.tick_params(axis="x", rotation=35)
        self.ax.grid(axis="y", color=GRID, linewidth=0.6)
        self.ax.set_axisbelow(True)
        self.fig.tight_layout()
        self.draw()
