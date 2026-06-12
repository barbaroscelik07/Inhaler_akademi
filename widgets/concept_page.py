"""D1 — Kavram sayfası şablonu.

Her bölüm için ortak düzen:
  Sol  : başlık, giriş, anahtar maddeler, aktif cihaza özgü not
  Sağ  : interaktif görsel (widget tipine göre) + MMAD/GSD kontrol paneli

Görsel tipleri content.py'deki "widget" alanından gelir:
  "ngi"          → NGIChart        (kademe deposizyon)
  "lung"         → LungChart       (akciğer bölge)
  "cmd"          → CMDChart        (kümülatif dağılım)
  "relationship" → RelationshipMap (ilişki haritası)
  None           → görsel yok, sadece metin (geniş)
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from core.device_profiles import get_device
from widgets.control_panel import ControlPanel
from widgets.interactive_ngi import NGIChart
from widgets.lung_deposition import LungChart
from widgets.cmd_plot import CMDChart
from widgets.relationship_map import RelationshipMap


_WIDGET_FACTORY = {
    "ngi": NGIChart,
    "lung": LungChart,
    "cmd": CMDChart,
    "relationship": RelationshipMap,
}


class ConceptPage(QWidget):
    def __init__(self, section: dict, device_key: str = "neb", parent=None):
        super().__init__(parent)
        self._section = section
        self._device_key = device_key
        self._widget_key = section.get("widget")

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ---------- SOL: metin ----------
        text_scroll = QScrollArea()
        text_scroll.setWidgetResizable(True)
        text_scroll.setFrameShape(QFrame.Shape.NoFrame)
        text_host = QWidget()
        tl = QVBoxLayout(text_host)
        tl.setContentsMargins(36, 32, 28, 32)
        tl.setSpacing(14)

        title = QLabel(section["title"])
        title.setObjectName("pageTitle")
        title.setWordWrap(True)
        tl.addWidget(title)

        lead = QLabel(section["lead"])
        lead.setObjectName("sectionLead")
        lead.setWordWrap(True)
        tl.addWidget(lead)

        # Anahtar maddeler
        for pt in section.get("points", []):
            row = QLabel(f"•  {pt}")
            row.setObjectName("bulletItem")
            row.setWordWrap(True)
            tl.addWidget(row)

        # Cihaza özgü not kartı
        self._device_card = QFrame()
        self._device_card.setObjectName("card")
        dc = QVBoxLayout(self._device_card)
        dc.setContentsMargins(14, 12, 14, 12)
        dc.setSpacing(4)
        self._device_title = QLabel()
        self._device_title.setObjectName("deviceNoteTitle")
        self._device_note = QLabel()
        self._device_note.setObjectName("sectionLead")
        self._device_note.setWordWrap(True)
        dc.addWidget(self._device_title)
        dc.addWidget(self._device_note)
        tl.addWidget(self._device_card)

        tl.addStretch()
        text_scroll.setWidget(text_host)
        root.addWidget(text_scroll, stretch=5)

        # ---------- SAĞ: görsel + kontrol ----------
        if self._widget_key in _WIDGET_FACTORY:
            right = QWidget()
            right.setObjectName("visualPanel")
            rl = QVBoxLayout(right)
            rl.setContentsMargins(20, 24, 28, 24)
            rl.setSpacing(14)

            self._chart = _WIDGET_FACTORY[self._widget_key]()
            rl.addWidget(self._chart, stretch=1)

            self._panel = ControlPanel(device_key=self._device_key)
            self._panel.changed.connect(self._on_values)
            rl.addWidget(self._panel)

            root.addWidget(right, stretch=4)
        else:
            self._chart = None
            self._panel = None

        self._refresh_device_note()
        self._render_initial()

    # ---- cihaz değişimi (sidebar'dan) ----
    def set_device(self, device_key: str):
        self._device_key = device_key
        self._refresh_device_note()
        if self._panel is not None:
            self._panel.set_device(device_key)  # değer + grafik yenilenir

    def _refresh_device_note(self):
        dev = get_device(self._device_key)
        note = self._section.get("devices", {}).get(self._device_key, "")
        self._device_title.setText(f"{dev.name} bağlamında")
        self._device_note.setText(note or dev.summary)

    def _render_initial(self):
        if self._chart is not None and self._panel is not None:
            mmad, gsd = self._panel.values
            dev = get_device(self._device_key)
            self._chart.update_plot(mmad, gsd, dev.typical_dose)

    def _on_values(self, mmad, gsd):
        if self._chart is not None:
            dev = get_device(self._device_key)
            self._chart.update_plot(mmad, gsd, dev.typical_dose)
