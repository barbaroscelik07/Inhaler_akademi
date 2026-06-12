"""
Kenar çubuğu: 14 bölüm navigasyonu + cihaz seçici (neb / pMDI / DPI).
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.device_profiles import DEVICE_ORDER, get_device


class Sidebar(QWidget):
    sectionSelected = pyqtSignal(int)   # bölüm index
    deviceChanged = pyqtSignal(str)     # cihaz key

    def __init__(self, sections, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self._current_device = DEVICE_ORDER[0]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QLabel("İnhaler APSD Akademi")
        header.setObjectName("sidebarHeader")
        layout.addWidget(header)

        sub = QLabel("Aerodinamik partikül parametreleri")
        sub.setObjectName("sidebarSub")
        sub.setWordWrap(True)
        layout.addWidget(sub)

        # --- Cihaz seçici ---
        dev_label = QLabel("CİHAZ")
        dev_label.setObjectName("deviceLabel")
        layout.addWidget(dev_label)

        dev_row = QWidget()
        dev_layout = QHBoxLayout(dev_row)
        dev_layout.setContentsMargins(14, 0, 14, 10)
        dev_layout.setSpacing(6)
        self._device_group = QButtonGroup(self)
        self._device_group.setExclusive(True)
        for i, key in enumerate(DEVICE_ORDER):
            btn = QPushButton(get_device(key).name)
            btn.setObjectName("deviceBtn")
            btn.setCheckable(True)
            btn.setChecked(i == 0)
            btn.clicked.connect(lambda _, k=key: self._on_device(k))
            self._device_group.addButton(btn)
            dev_layout.addWidget(btn)
        layout.addWidget(dev_row)

        # --- Bölüm listesi ---
        self.nav = QListWidget()
        self.nav.setObjectName("navList")
        for sec in sections:
            QListWidgetItem(sec["title"], self.nav)
        self.nav.currentRowChanged.connect(self.sectionSelected.emit)
        layout.addWidget(self.nav, stretch=1)

    def _on_device(self, key: str):
        self._current_device = key
        self.deviceChanged.emit(key)

    @property
    def current_device(self) -> str:
        return self._current_device

    def select_first(self):
        if self.nav.count():
            self.nav.setCurrentRow(0)
