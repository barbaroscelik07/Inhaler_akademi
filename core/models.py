"""
APSD hesaplama motoru.

Temel yaklaşım: Aerodinamik partikül boyut dağılımı log-normal kabul edilir.
Bir log-normal dağılım MMAD (medyan) ve GSD (geometrik standart sapma) ile
tam olarak tanımlanır. Bu iki parametreden:
  - NGI kademe (stage) deposizyon profili
  - Kümülatif kütle dağılımı (CMD)
  - FPF, FPD, RF, EFPF
  - Akciğer bölge deposizyon tahmini
türetilir.

Referanslar: Ph. Eur. 2.9.18, USP <601>.
NGI kesim çapları akış hızına bağlıdır; burada 60 L/dk için arşivlenmiş
nominal değerler kullanılır (eğitim amaçlı yaklaşık değerler).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List

from scipy.stats import lognorm


# NGI kademe kesim çapları (µm) — 60 L/dk nominal.
# Her kademe, kendisinden büyük partikülleri tutar; sıralı azalan kesim.
NGI_CUTOFFS_60 = {
    "Stage 1": 8.06,
    "Stage 2": 4.46,
    "Stage 3": 2.82,
    "Stage 4": 1.66,
    "Stage 5": 0.94,
    "Stage 6": 0.55,
    "Stage 7": 0.34,
    "MOC": 0.0,  # Micro-Orifice Collector: kalan tüm ince partiküller
}

# Akciğer deposizyon bölgeleri (aerodinamik çap aralıkları, µm).
LUNG_REGIONS = [
    ("Ağız / Boğaz", 10.0, float("inf")),
    ("Üst solunum yolu", 5.0, 10.0),
    ("Bronşiyal / Bronşiyolar", 1.0, 5.0),
    ("Alveolar", 0.5, 1.0),
    ("Ekshalasyon (<0.5)", 0.0, 0.5),
]

# Parametre eşikleri (µm).
FPF_THRESHOLD = 5.0      # İnce partikül: < 5 µm
EFPF_THRESHOLD = 2.0     # Ekstra ince partikül: < 2 µm
RF_LOWER = 1.0           # Solunabilir fraksiyon alt sınır
RF_UPPER = 5.0           # Solunabilir fraksiyon üst sınır


@dataclass
class APSDResult:
    """Bir MMAD/GSD/doz kombinasyonu için hesaplanmış tüm çıktılar."""

    mmad: float
    gsd: float
    total_dose: float                       # µg, yüklenen toplam doz
    stage_fractions: Dict[str, float] = field(default_factory=dict)  # %
    stage_mass: Dict[str, float] = field(default_factory=dict)       # µg
    cumulative_undersize: List[tuple] = field(default_factory=list)  # (çap, %)
    region_fractions: Dict[str, float] = field(default_factory=dict) # %
    fpf: float = 0.0   # %
    efpf: float = 0.0  # %
    rf: float = 0.0    # %
    fpd: float = 0.0   # µg


def _lognorm_dist(mmad: float, gsd: float):
    """SciPy log-normal dağılım nesnesi.

    shape parametresi s = ln(GSD); scale = MMAD (medyan).
    """
    gsd = max(gsd, 1.001)
    s = math.log(gsd)
    return lognorm(s=s, scale=mmad)


def fraction_below(mmad: float, gsd: float, diameter: float) -> float:
    """Verilen çapın altındaki kütle fraksiyonu (0-1)."""
    if diameter <= 0:
        return 0.0
    if diameter == float("inf"):
        return 1.0
    return float(_lognorm_dist(mmad, gsd).cdf(diameter))


def fraction_between(mmad: float, gsd: float, low: float, high: float) -> float:
    """[low, high) aralığındaki kütle fraksiyonu (0-1)."""
    return fraction_below(mmad, gsd, high) - fraction_below(mmad, gsd, low)


def compute_apsd(mmad: float, gsd: float, total_dose: float = 1000.0) -> APSDResult:
    """MMAD ve GSD'den tam APSD profilini hesapla."""
    res = APSDResult(mmad=mmad, gsd=gsd, total_dose=total_dose)

    # --- NGI kademe dağılımı ---
    # Sıralı kesim çapları (büyükten küçüğe). Her kademe iki ardışık
    # kesim arasındaki kütleyi toplar.
    cutoffs = list(NGI_CUTOFFS_60.items())
    upper = float("inf")
    for name, lower in cutoffs:
        frac = fraction_between(mmad, gsd, lower, upper)
        res.stage_fractions[name] = frac * 100.0
        res.stage_mass[name] = frac * total_dose
        upper = lower

    # --- Kümülatif undersize eğrisi (CMD) ---
    diameters = [0.2, 0.34, 0.55, 0.94, 1.66, 2.82, 4.46, 8.06, 12.0, 20.0]
    res.cumulative_undersize = [
        (d, fraction_below(mmad, gsd, d) * 100.0) for d in diameters
    ]

    # --- Akciğer bölge deposizyonu ---
    for name, low, high in LUNG_REGIONS:
        res.region_fractions[name] = (
            fraction_between(mmad, gsd, low, high) * 100.0
        )

    # --- Türetilmiş parametreler ---
    res.fpf = fraction_below(mmad, gsd, FPF_THRESHOLD) * 100.0
    res.efpf = fraction_below(mmad, gsd, EFPF_THRESHOLD) * 100.0
    res.rf = fraction_between(mmad, gsd, RF_LOWER, RF_UPPER) * 100.0
    res.fpd = (res.fpf / 100.0) * total_dose

    return res


def gsd_band(mmad: float, gsd: float) -> tuple:
    """GSD'nin sezgisel 'kat' yorumu: ortalamanın 1/GSD ile GSD katı arası."""
    return (mmad / gsd, mmad * gsd)


def classify_gsd(gsd: float) -> str:
    """Word'deki GSD yorumlama tablosuna göre dağılım tipi."""
    if gsd <= 1.0:
        return "Monodispers (ideal)"
    if gsd <= 1.5:
        return "Dar polidispers"
    if gsd <= 2.5:
        return "Orta polidispers (tipik)"
    if gsd <= 3.5:
        return "Geniş polidispers"
    return "Çok geniş dağılım"


def mmad_target_zone(mmad: float) -> str:
    """MMAD'nin hedef pencereye göre değerlendirmesi."""
    if mmad < 1.0:
        return "Çok küçük — ekshalasyon riski"
    if mmad <= 3.0:
        return "Alveolar / derin akciğer"
    if mmad <= 5.0:
        return "Bronşiyal — optimal pencere"
    if mmad <= 10.0:
        return "Üst solunum yolu ağırlıklı"
    return "Ağız/boğaz depozisyonu baskın"
