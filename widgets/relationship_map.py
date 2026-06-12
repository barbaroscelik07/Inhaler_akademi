"""C4 — Parametreler arası ilişki şeması (canlı değerlerle).

Kavram haritası: girdi parametreleri (MMAD, GSD) → türetilmiş parametreler
(FPF, RF, EFPF, FPD) → klinik sonuç (akciğer deposizyonu). Oklarla bağlanır,
düğümlerde canlı hesaplanan değerler gösterilir.

Matplotlib ile çizilir (mevcut canvas altyapısıyla tutarlı; ek bağımlılık yok).
"""

from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from widgets.mpl_canvas import (
    ACCENT,
    ACCENT_DARK,
    GRID,
    INK,
    MUTED,
    SURFACE,
    WARN,
    MplCanvas,
)
from core.models import compute_apsd, mmad_target_zone


def _node(ax, x, y, w, h, title, value, fill, edge, text_color="#FFFFFF"):
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        linewidth=1.2, facecolor=fill, edgecolor=edge, zorder=2,
    )
    ax.add_patch(box)
    ax.text(x, y + h * 0.16, title, ha="center", va="center",
            fontsize=8.5, fontweight="bold", color=text_color, zorder=3)
    ax.text(x, y - h * 0.22, value, ha="center", va="center",
            fontsize=9.5, color=text_color, zorder=3)


def _arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=12,
        linewidth=1.3, color=MUTED, zorder=1,
        shrinkA=2, shrinkB=2,
    ))


class RelationshipMap(MplCanvas):
    def __init__(self):
        super().__init__(width=5.6, height=3.8)

    def update_plot(self, mmad, gsd, total_dose=1000.0):
        r = compute_apsd(mmad, gsd, total_dose)
        self.clear()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.axis("off")
        self.ax.set_title("Parametre İlişki Haritası", fontsize=10, loc="left")

        # --- Girdi düğümleri (sol) ---
        _node(self.ax, 1.7, 7.5, 2.6, 1.5, "MMAD",
              f"{mmad:.1f} µm", ACCENT_DARK, ACCENT_DARK)
        _node(self.ax, 1.7, 4.0, 2.6, 1.5, "GSD",
              f"{gsd:.2f}", ACCENT_DARK, ACCENT_DARK)

        # --- Türetilmiş düğümler (orta) ---
        _node(self.ax, 5.0, 8.3, 2.4, 1.3, "FPF (<5µm)",
              f"%{r.fpf:.0f}", ACCENT, ACCENT)
        _node(self.ax, 5.0, 6.2, 2.4, 1.3, "RF (1–5µm)",
              f"%{r.rf:.0f}", ACCENT, ACCENT)
        _node(self.ax, 5.0, 4.1, 2.4, 1.3, "EFPF (<2µm)",
              f"%{r.efpf:.0f}", ACCENT, ACCENT)
        _node(self.ax, 5.0, 2.0, 2.4, 1.3, "FPD",
              f"{r.fpd:.0f} µg", ACCENT, ACCENT)

        # --- Sonuç düğümü (sağ) ---
        bronsial = r.region_fractions.get("Bronşiyal / Bronşiyolar", 0.0)
        _node(self.ax, 8.5, 5.2, 2.6, 1.8, "Akciğer",
              f"%{bronsial:.0f} bronşiyal", WARN, WARN)

        # --- Oklar ---
        for (sy) in (8.3, 6.2, 4.1, 2.0):
            _arrow(self.ax, 3.0, 7.5, 3.8, sy)   # MMAD → türetilmiş
            _arrow(self.ax, 3.0, 4.0, 3.8, sy)   # GSD → türetilmiş
        for (sy) in (8.3, 6.2, 4.1, 2.0):
            _arrow(self.ax, 6.2, sy, 7.2, 5.2)   # türetilmiş → akciğer

        # Alt açıklama
        self.fig.text(
            0.5, 0.02,
            f"MMAD ve GSD birlikte tüm türetilmiş parametreleri belirler "
            f"· {mmad_target_zone(mmad)}",
            ha="center", fontsize=7.5, color=MUTED,
        )
        self.fig.tight_layout(rect=(0, 0.05, 1, 1))
        self.draw()
