"""
Ortak kontrol paneli: MMAD ve GSD kaydırıcıları + canlı metrik okumaları.
İnteraktif görseller bu paneli paylaşır; değer değişince sinyal yayar.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from core.device_profiles import get_device
from core.models import classify_gsd, compute_apsd, gsd_band, mmad_target_zone


class _Metric(QWidget):
    def __init__(self, label):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 6, 8, 6)
        lay.setSpacing(0)
        self.value = QLabel("—")
        self.value.setObjectName("metricValue")
        cap = QLabel(label)
        cap.setObjectName("metricLabel")
        lay.addWidget(self.value)
        lay.addWidget(cap)

    def set(self, text):
        self.value.setText(text)


class ControlPanel(QWidget):
    """MMAD + GSD kaydırıcıları ve canlı metrikler."""

    changed = pyqtSignal(float, float)  # mmad, gsd

    def __init__(self, device_key="neb", parent=None):
        super().__init__(parent)
        self._device_key = device_key
        dev = get_device(device_key)
        self._mmad = dev.mmad_default
        self._gsd = dev.gsd_default

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        # --- MMAD slider ---
        self._mmad_head = QLabel()
        root.addWidget(self._mmad_head)
        self.mmad_slider = QSlider(Qt.Orientation.Horizontal)
        self.mmad_slider.setMinimum(int(dev.mmad_min * 10))
        self.mmad_slider.setMaximum(int(dev.mmad_max * 10))
        self.mmad_slider.setValue(int(self._mmad * 10))
        self.mmad_slider.valueChanged.connect(self._on_mmad)
        root.addWidget(self.mmad_slider)

        # --- GSD slider ---
        self._gsd_head = QLabel()
        root.addWidget(self._gsd_head)
        self.gsd_slider = QSlider(Qt.Orientation.Horizontal)
        self.gsd_slider.setMinimum(int(dev.gsd_min * 100))
        self.gsd_slider.setMaximum(int(dev.gsd_max * 100))
        self.gsd_slider.setValue(int(self._gsd * 100))
        self.gsd_slider.valueChanged.connect(self._on_gsd)
        root.addWidget(self.gsd_slider)

        # --- Metrikler ---
        grid = QFrame()
        grid.setObjectName("card")
        gl = QGridLayout(grid)
        gl.setContentsMargins(8, 8, 8, 8)
        gl.setSpacing(4)
        self.m_fpf = _Metric("FPF (<5 µm)")
        self.m_rf = _Metric("RF (1–5 µm)")
        self.m_efpf = _Metric("EFPF (<2 µm)")
        self.m_fpd = _Metric("FPD (µg)")
        gl.addWidget(self.m_fpf, 0, 0)
        gl.addWidget(self.m_rf, 0, 1)
        gl.addWidget(self.m_efpf, 1, 0)
        gl.addWidget(self.m_fpd, 1, 1)
        root.addWidget(grid)

        self._interp = QLabel()
        self._interp.setObjectName("sectionLead")
        self._interp.setWordWrap(True)
        root.addWidget(self._interp)
        root.addStretch()

        self._refresh_labels()

    # --- cihaz değişimi ---
    def set_device(self, device_key):
        self._device_key = device_key
        dev = get_device(device_key)
        for sl, lo, hi, val, scale in (
            (self.mmad_slider, dev.mmad_min, dev.mmad_max, dev.mmad_default, 10),
            (self.gsd_slider, dev.gsd_min, dev.gsd_max, dev.gsd_default, 100),
        ):
            sl.blockSignals(True)
            sl.setMinimum(int(lo * scale))
            sl.setMaximum(int(hi * scale))
            sl.setValue(int(val * scale))
            sl.blockSignals(False)
        self._mmad = dev.mmad_default
        self._gsd = dev.gsd_default
        self._refresh_labels()
        self.changed.emit(self._mmad, self._gsd)

    def _on_mmad(self, v):
        self._mmad = v / 10.0
        self._refresh_labels()
        self.changed.emit(self._mmad, self._gsd)

    def _on_gsd(self, v):
        self._gsd = v / 100.0
        self._refresh_labels()
        self.changed.emit(self._mmad, self._gsd)

    def _refresh_labels(self):
        self._mmad_head.setText(
            f"<b>MMAD</b> = {self._mmad:.1f} µm  "
            f"<span style='color:#52606D;'>· {mmad_target_zone(self._mmad)}</span>"
        )
        lo, hi = gsd_band(self._mmad, self._gsd)
        self._gsd_head.setText(
            f"<b>GSD</b> = {self._gsd:.2f}  "
            f"<span style='color:#52606D;'>· {classify_gsd(self._gsd)} "
            f"(≈{lo:.1f}–{hi:.1f} µm)</span>"
        )
        dev = get_device(self._device_key)
        r = compute_apsd(self._mmad, self._gsd, dev.typical_dose)
        self.m_fpf.set(f"{r.fpf:.0f}%")
        self.m_rf.set(f"{r.rf:.0f}%")
        self.m_efpf.set(f"{r.efpf:.0f}%")
        self.m_fpd.set(f"{r.fpd:.0f}")
        self._interp.setText(
            f"Bu profilde dozun ~%{r.fpf:.0f}'i akciğere ulaşabilen ince "
            f"partikül (<5 µm), ~%{r.rf:.0f}'i optimal solunabilir aralıkta "
            f"(1–5 µm). {dev.name} test akış hızı: {dev.flow_rate}."
        )

    @property
    def values(self):
        return self._mmad, self._gsd
