"""Matplotlib + PyQt6 ortak canvas tabanı (klinik tema renkleri)."""

import matplotlib
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# Klinik tema paleti (theme.qss ile uyumlu)
ACCENT = "#0E7C86"
ACCENT_DARK = "#0A5C63"
INK = "#1F2933"
MUTED = "#52606D"
GRID = "#E2E8F0"
WARN = "#C2410C"
SURFACE = "#FFFFFF"

# Akciğer bölge renkleri
REGION_COLORS = {
    "Ağız / Boğaz": "#C2410C",
    "Üst solunum yolu": "#D9822B",
    "Bronşiyal / Bronşiyolar": "#0E7C86",
    "Alveolar": "#2B8A9E",
    "Ekshalasyon (<0.5)": "#9AA5B1",
}


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5.0, height=3.5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=SURFACE)
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self._style_axes()

    def _style_axes(self):
        self.ax.set_facecolor(SURFACE)
        for spine in ("top", "right"):
            self.ax.spines[spine].set_visible(False)
        for spine in ("left", "bottom"):
            self.ax.spines[spine].set_color(GRID)
        self.ax.tick_params(colors=MUTED, labelsize=8)
        self.ax.yaxis.label.set_color(MUTED)
        self.ax.xaxis.label.set_color(MUTED)
        self.ax.title.set_color(INK)

    def clear(self):
        # Figure seviyesindeki yazıları (fig.text) da temizle; aksi halde
        # her güncellemede birikip üst üste binerler.
        self.fig.texts.clear()
        self.ax.clear()
        self._style_axes()
