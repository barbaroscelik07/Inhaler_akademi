"""C2 — Akciğer bölge deposizyon diyagramı (canlı).

MMAD/GSD'den hesaplanan bölge fraksiyonlarını yatay bir anatomik
"derinlik" çubuğu olarak gösterir: ağız/boğaz → üst solunum yolu →
bronşiyal → alveolar → ekshalasyon. Her bölgenin yüzdesi canlı güncellenir.
"""

from widgets.mpl_canvas import GRID, INK, MUTED, REGION_COLORS, MplCanvas
from core.models import LUNG_REGIONS, compute_apsd


# Diyagramda gösterim sırası (üstten alta = iri partikülden ince partiküle,
# yani anatomik olarak ağızdan alveole doğru).
_ORDER = [name for name, _, _ in LUNG_REGIONS]


class LungChart(MplCanvas):
    def __init__(self):
        super().__init__(width=5.4, height=3.6)

    def update_plot(self, mmad, gsd, total_dose=1000.0):
        r = compute_apsd(mmad, gsd, total_dose)
        self.clear()

        labels = _ORDER
        vals = [r.region_fractions.get(name, 0.0) for name in labels]
        colors = [REGION_COLORS.get(name, "#9AA5B1") for name in labels]

        y_pos = range(len(labels))
        bars = self.ax.barh(list(y_pos), vals, color=colors, height=0.66)
        self.ax.set_yticks(list(y_pos))
        self.ax.set_yticklabels(labels, fontsize=8)
        self.ax.invert_yaxis()  # ağız/boğaz en üstte
        self.ax.set_xlabel("Kütle fraksiyonu (%)")
        self.ax.set_title("Akciğer Bölge Deposizyon Tahmini",
                          fontsize=10, loc="left")
        self.ax.set_xlim(0, max(vals) * 1.25 + 1)

        for b, v in zip(bars, vals):
            if v >= 0.5:
                self.ax.text(v + max(vals) * 0.02 + 0.2,
                             b.get_y() + b.get_height() / 2,
                             f"{v:.0f}%", va="center", ha="left",
                             fontsize=8, color=INK)

        self.ax.grid(axis="x", color=GRID, linewidth=0.6)
        self.ax.set_axisbelow(True)

        # Optimal pencere (1–5 µm = bronşiyal) vurgusu altyazı
        self.fig.text(
            0.5, 0.01,
            "Optimal terapötik pencere: 1–5 µm (bronşiyal/bronşiyolar)",
            ha="center", fontsize=7.5, color=MUTED,
        )
        self.fig.tight_layout(rect=(0, 0.04, 1, 1))
        self.draw()
