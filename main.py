"""
İnhaler APSD Akademi
Aerodinamik Partikül Boyut Dağılımı (APSD) interaktif eğitim programı.
Nebülizer / pMDI / DPI cihazları için MMAD, GSD, FPF, FPD, EFPF, RF ve
NGI deposizyon parametrelerini görsel ve etkileşimli olarak öğretir.

Designed by Barbaros Çelik
"""

import os
import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QWidget,
)

from core.content import SECTIONS
from widgets.concept_page import ConceptPage
from widgets.sidebar import Sidebar


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_stylesheet() -> str:
    qss_path = os.path.join(BASE_DIR, "assets", "theme.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as fh:
            return fh.read()
    return ""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("İnhaler APSD Akademi")
        self.resize(1320, 820)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.stack = QStackedWidget()
        self.sidebar = Sidebar(SECTIONS)

        # 14 bölüm için gerçek kavram sayfaları
        self._pages = []
        start_device = self.sidebar.current_device
        for section in SECTIONS:
            page = ConceptPage(section, device_key=start_device)
            self._pages.append(page)
            self.stack.addWidget(page)

        # Navigasyon + cihaz sinyalleri
        self.sidebar.sectionSelected.connect(self.stack.setCurrentIndex)
        self.sidebar.deviceChanged.connect(self._on_device_changed)

        root.addWidget(self.sidebar)
        root.addWidget(self.stack, stretch=1)

        self.sidebar.select_first()

    def _on_device_changed(self, device_key: str):
        # Tüm sayfaları yeni cihaza göre güncelle
        for page in self._pages:
            page.set_device(device_key)


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(load_stylesheet())
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
