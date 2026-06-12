"""
Cihaz profilleri: Nebülizer, pMDI, DPI.

Her cihaz için tipik MMAD/GSD aralıkları, NGI test akış hızı, başlangıç
(varsayılan) değerleri ve cihaza özgü eğitim notları tutulur. Değerler
literatür ve regülatör kılavuzlardan (Ph. Eur. 2.9.18, EMA OIP, FDA OIP)
derlenmiş tipik aralıklardır; eğitim amaçlıdır.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceProfile:
    key: str
    name: str
    full_name: str
    flow_rate: str            # NGI test akış hızı
    mmad_min: float
    mmad_max: float
    mmad_default: float
    gsd_min: float
    gsd_max: float
    gsd_default: float
    typical_dose: float       # µg (eğitim ölçeği)
    summary: str
    key_factors: tuple        # MMAD'yi etkileyen ana faktörler
    note: str                 # Cihaza özgü APSD notu


NEBULIZER = DeviceProfile(
    key="neb",
    name="Nebülizer",
    full_name="Nebülizatör (jet / mesh / ultrasonik)",
    flow_rate="15 L/dk (nebülizer kurulumu)",
    mmad_min=1.0,
    mmad_max=8.0,
    mmad_default=3.5,
    gsd_min=1.5,
    gsd_max=3.0,
    gsd_default=2.2,
    typical_dose=1000.0,
    summary=(
        "Sıvı formülasyonu sürekli aerosole çevirir; düşük inspirasyon "
        "eforu gerektirir, pediatrik ve yoğun bakım hastalarında tercih "
        "edilir. APSD; mesh boyutu, titreşim frekansı ve formülasyon "
        "viskozitesi tarafından belirlenir."
    ),
    key_factors=(
        "Mesh delik boyutu / nozül geometrisi",
        "Titreşim frekansı (mesh / ultrasonik)",
        "Formülasyon viskozitesi ve yüzey gerilimi",
        "Süspansiyon partikül boyutu (süspansiyon ürünlerde)",
    ),
    note=(
        "Nebülizasyon süspansiyonlarında damlacık birden fazla katı "
        "partikül içerebilir; bu nedenle ölçülen aerodinamik çap, ham "
        "partikül boyutundan büyük olabilir."
    ),
)

PMDI = DeviceProfile(
    key="pmdi",
    name="pMDI",
    full_name="Basınçlı Ölçülü Doz İnhalatörü (pMDI)",
    flow_rate="28.3 L/dk (pMDI kurulumu)",
    mmad_min=0.8,
    mmad_max=6.0,
    mmad_default=2.8,
    gsd_min=1.4,
    gsd_max=2.2,
    gsd_default=1.7,
    typical_dose=200.0,
    summary=(
        "İticisi (propellant) ile sabit ölçülü doz püskürtür. APSD; "
        "aktüatör orifis çapı, sprey açısı ve propellant buharlaşması ile "
        "şekillenir. El-nefes koordinasyonu gerektirir; spacer kullanımı "
        "üst solunum yolu kaybını azaltır."
    ),
    key_factors=(
        "Aktüatör orifis çapı",
        "Sprey açısı ve püskürtme hızı",
        "Propellant tipi ve buharlaşma hızı",
        "Eş-çözücü (etanol) oranı",
    ),
    note=(
        "Solüsyon pMDI'larda buharlaşma sonrası kalıntı partikül boyutu "
        "küçük olur; süspansiyon pMDI'larda ham partikül boyutu MMAD'yi "
        "doğrudan etkiler."
    ),
)

DPI = DeviceProfile(
    key="dpi",
    name="DPI",
    full_name="Kuru Toz İnhalatörü (DPI)",
    flow_rate="60 L/dk (DPI kurulumu, 4 kPa)",
    mmad_min=1.0,
    mmad_max=7.0,
    mmad_default=3.2,
    gsd_min=1.6,
    gsd_max=2.6,
    gsd_default=2.0,
    typical_dose=400.0,
    summary=(
        "Hastanın inspirasyon eforuyla tozu de-aglomere eder; itici "
        "içermez. APSD; cihaz rezistansı, hastanın akış hızı ve toz "
        "formülasyonunun (taşıyıcı-API) ayrışma verimine bağlıdır. "
        "Akışa bağımlılık DPI'ların en kritik özelliğidir."
    ),
    key_factors=(
        "Cihaz iç rezistansı",
        "Hasta inspirasyon akış hızı (de-aglomerasyon)",
        "Taşıyıcı (laktoz) - API yapışma kuvveti",
        "Mikronizasyon / partikül mühendisliği",
    ),
    note=(
        "DPI performansı akış hızına güçlü bağımlıdır; APSD farklı akış "
        "hızlarında (örn. düşük eforu temsilen) test edilmelidir."
    ),
)

DEVICES = {d.key: d for d in (NEBULIZER, PMDI, DPI)}
DEVICE_ORDER = ["neb", "pmdi", "dpi"]


def get_device(key: str) -> DeviceProfile:
    return DEVICES.get(key, NEBULIZER)
