# İnhaler APSD Akademi

Aerodinamik Partikül Boyut Dağılımı (APSD) parametrelerini **interaktif ve
görsel** olarak öğreten PyQt6 masaüstü eğitim programı. Nebülizer, pMDI ve
DPI cihazları bağlamında MMAD, GSD, FPF, FPD, EFPF, RF ve NGI deposizyon
profillerini canlı simülasyonlarla ele alır.

> Designed by Barbaros Çelik

## Amaç

Kullanıcı MMAD ve GSD kaydırıcılarını oynattıkça; NGI kademe deposizyonu,
akciğer bölge dağılımı, kümülatif kütle eğrisi ve parametre ilişki haritası
**anlık** olarak güncellenir. Böylece parametreler arası ilişki ezberle değil,
deneyerek kavranır.

İçerik 14 bölümden oluşur ve her parametre üç cihaz tipi (nebülizer / pMDI /
DPI) bağlamında karşılaştırmalı olarak sunulur. Metinler Ph. Eur. 2.9.18 ve
USP <601> çerçeveli kaynak dokümandan özetlenmiş ve programa gömülüdür
(çevrimdışı çalışır).

## Bölümler

1. Giriş ve Kapsam
2. MMAD (Kütle Medyan Aerodinamik Çap)
3. GSD (Geometrik Standart Sapma)
4. FPD ve FPF (İnce Partikül Doz/Fraksiyon)
5. EFPF (Ekstra İnce Partikül Fraksiyonu)
6. RF (Solunabilir Fraksiyon)
7. APSD (Aerodinamik Partikül Boyut Dağılımı)
8. Kümülatif Kütle Dağılımı (CMD)
9. NGI Toplam Geri Kazanım
10. NGI Stage Deposizyon Profili (1–7)
11. İndüksiyon Port Deposizyonu
12. Pre-Separatör Deposizyonu
13. Kalite Sistemi ve Regülatör Çerçeve
14. Sonuç ve Öneriler

## İnteraktif Görseller

| Görsel | Açıklama |
|--------|----------|
| NGI Kademe Profili | MMAD/GSD → 8 kademe (S1–S7 + MOC) kütle dağılımı |
| Akciğer Bölge Deposizyonu | Ağız/boğaz → üst yol → bronşiyal → alveolar → ekshalasyon |
| Kümülatif Kütle Dağılımı | Log-eksende CMD; %50 kesişimi MMAD'yi verir, d₁₆/d₈₄ ile GSD |
| Parametre İlişki Haritası | MMAD/GSD → FPF/RF/EFPF/FPD → akciğer deposizyonu akışı |

## Hesaplama Modeli

APSD log-normal dağılım kabul edilir; MMAD (medyan) ve GSD (ln-SS'nin
eksponansiyeli) ile tam tanımlanır. NGI kesim çapları 60 L/dk nominal
değerlerle alınır. Türetilen tüm parametreler (FPF <5 µm, EFPF <2 µm,
RF 1–5 µm, FPD) bu dağılımdan SciPy `lognorm` ile hesaplanır.

> Değerler eğitim amaçlıdır; gerçek ürün kararları için validasyonlu ölçüm
> verisi esastır.

## Klasör Yapısı

```
InhalerAPSD-Akademi/
├── main.py                      # QMainWindow, navigasyon + sayfa yönetimi
├── core/
│   ├── models.py                # log-normal APSD hesaplama motoru
│   ├── device_profiles.py       # neb / pMDI / DPI parametre setleri
│   └── content.py               # 14 bölüm gömülü eğitim metni
├── widgets/
│   ├── sidebar.py               # bölüm navigasyonu + cihaz seçici
│   ├── concept_page.py          # metin + görsel sayfa şablonu
│   ├── control_panel.py         # MMAD/GSD kaydırıcı + canlı metrikler
│   ├── mpl_canvas.py            # Matplotlib taban canvas (klinik tema)
│   ├── interactive_ngi.py       # NGI kademe grafiği
│   ├── lung_deposition.py       # akciğer bölge diyagramı
│   ├── cmd_plot.py              # kümülatif kütle / log-olasılık eğrisi
│   └── relationship_map.py      # parametre ilişki haritası
├── assets/theme.qss             # sade modern klinik tema
└── .github/workflows/build.yml  # PyInstaller → Windows .exe
```

## Çalıştırma (geliştirme)

```bash
pip install -r requirements.txt
python main.py
```

## Windows EXE

`v*` etiketi (tag) push edildiğinde veya Actions sekmesinden manuel
tetiklendiğinde GitHub Actions + PyInstaller ile tek dosyalık `.exe` üretilir
ve artifact olarak yüklenir; tag varsa release'e eklenir.

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Referanslar

Ph. Eur. 2.9.18 · USP <601> · EMA OIP kılavuzları · FDA OIP rehberleri
