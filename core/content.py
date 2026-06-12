"""
Gömülü eğitim içeriği — 14 bölüm.

Her bölüm:
  id        : benzersiz anahtar
  title     : kenar çubuğu / başlık metni
  lead      : kısa giriş paragrafı
  points    : madde madde anahtar bilgiler
  devices   : {cihaz_key: cihaza özgü kısa not}
  widget    : sayfaya eklenecek interaktif görsel anahtarı
               ("ngi", "lung", "cmd", "relationship", None)

Metinler kaynak Word dokümanından (Ph. Eur. 2.9.18 / USP <601> çerçeveli)
özetlenmiş, nebülizer + pMDI + DPI bağlamına genişletilmiştir.
"""

SECTIONS = [
    {
        "id": "intro",
        "title": "1. Giriş ve Kapsam",
        "lead": (
            "İnhaler ilaç tasarımı, aktif maddenin aerosol partikülleri olarak "
            "solunum yoluna etkin biçimde iletilmesini hedefler. Aerodinamik "
            "partikül karakterizasyonu, formülasyonun klinik etkinliğini "
            "doğrudan belirleyen en kritik kalite parametresidir."
        ),
        "points": [
            "Deposizyon yeri; partikül boyutu, yoğunluğu, şekli, solunum hızı "
            "ve hasta anatomisine bağlıdır.",
            "Next Generation Impactor (NGI) ve kaskad impaktör yöntemleri "
            "aerodinamik karakterizasyonda altın standarttır.",
            "Tüm analizler Ph. Eur. 2.9.18 ve USP <601> çerçevesinde, "
            "standardize ölçüm koşullarında (akış hızı, nem, sıcaklık) "
            "değerlendirilir.",
            "Bu program 14 temel parametreyi nebülizer, pMDI ve DPI bağlamında "
            "etkileşimli olarak ele alır.",
        ],
        "devices": {
            "neb": "Sürekli aerosol; düşük inspirasyon eforu.",
            "pmdi": "İticisiyle sabit ölçülü doz; koordinasyon gerekir.",
            "dpi": "Hastanın eforuyla de-aglomerasyon; akışa bağımlı.",
        },
        "widget": "relationship",
    },
    {
        "id": "mmad",
        "title": "2. MMAD (Kütle Medyan Aerodinamik Çap)",
        "lead": (
            "MMAD, aerosol partiküllerinin aerodinamik çap dağılımının medyan "
            "değeridir: partiküllerin kütlece %50'si bu çaptan küçük, %50'si "
            "büyüktür. Aerodinamik çap, partikülün havadaki hareketini "
            "belirleyen etkili çaptır (1 g/cm³ küresel partikül eşdeğeri)."
        ),
        "points": [
            "0.5–1 µm: alveolar bölge, sistemik emilim.",
            "1–5 µm: bronşiyal/bronşiyolar bölge, lokal etki — optimal pencere.",
            "5–10 µm: üst solunum yolları.",
            ">10 µm: ağız/boğaz depozisyonu, yutulur.",
            "İnhaler ürünler için optimal MMAD genellikle 1–5 µm'dir.",
            "Batch-to-batch ±%20 tolerans tipik QC kriteridir.",
        ],
        "devices": {
            "neb": "Mesh boyutu, titreşim frekansı ve viskozite MMAD'yi belirler.",
            "pmdi": "Aktüatör orifis çapı, sprey açısı ve propellant etkili.",
            "dpi": "İnhaler rezistansı, akış hızı ve de-aglomerasyon belirleyici.",
        },
        "widget": "lung",
    },
    {
        "id": "gsd",
        "title": "3. GSD (Geometrik Standart Sapma)",
        "lead": (
            "GSD, log-normal dağılımda yayılımı 'kat' mantığıyla ifade eden "
            "boyutsuz parametredir. GSD ≥ 1; 1.0 monodisperstir. GSD=2.0 ise "
            "ana kütle, ortalama çapın yarısı ile iki katı arasındadır."
        ),
        "points": [
            "GSD = d₈₄.₁ / d₅₀ = d₅₀ / d₁₅.₉ (Hatch–Choate).",
            "Aritmetik SS mutlak farkı, GSD oransal (çarpan) farkı ölçer.",
            "1.0–1.5 dar; 1.5–2.5 orta (tipik); 2.5–3.5 geniş; >3.5 çok geniş.",
            "Aynı MMAD'de yüksek GSD → hem iri hem ince partikül artar, "
            "akciğer deposizyon verimi düşer.",
            "Log-olasılık grafiğinde regresyon eğiminin doğrusallığı "
            "log-normalliği teyit eder.",
        ],
        "devices": {
            "neb": "Tipik GSD 1.8–2.5; jet nebülizerde dar GSD nadirdir.",
            "pmdi": "Solüsyon pMDI'larda daha dar GSD (≈1.4–2.0) elde edilebilir.",
            "dpi": "De-aglomerasyon verimi GSD'yi etkiler; akışa duyarlıdır.",
        },
        "widget": "ngi",
    },
    {
        "id": "fpf_fpd",
        "title": "4. FPD ve FPF (İnce Partikül Doz/Fraksiyon)",
        "lead": (
            "FPD, aerodinamik çapı < 5 µm olan partiküllerdeki toplam ilaç "
            "miktarıdır (µg). FPF ise bu ince partikül kütlesinin toplam doza "
            "oranıdır (%). İkisi de alt solunum yoluna ulaşabilen dozu tanımlar."
        ),
        "points": [
            "FPD = Σ (d < 5 µm aşama kütleleri); IP ve pre-separatör hariç.",
            "FPF = FPD / toplam doz × 100.",
            "Bazı standartlarda kesim 4.7 µm alınır (Ph. Eur. 2.9.18).",
            "Yüksek FPF → akciğere daha iyi penetrasyon.",
            "FPF, MMAD ve GSD ile birlikte yorumlanmalıdır.",
        ],
        "devices": {
            "neb": "Süspansiyonlarda damlacık çok partikül içerebilir; FPD'yi etkiler.",
            "pmdi": "Spacer kullanımı IP kaybını azaltır, etkili FPD artar.",
            "dpi": "Düşük akış → zayıf de-aglomerasyon → düşük FPF.",
        },
        "widget": "ngi",
    },
    {
        "id": "efpf",
        "title": "5. EFPF (Ekstra İnce Partikül Fraksiyonu)",
        "lead": (
            "EFPF, aerodinamik çapı genellikle < 2 µm olan partiküllerin "
            "fraksiyonudur. Küçük havayolları ve periferik akciğer hedeflemesi "
            "için kritik biyolojik öneme sahiptir."
        ),
        "points": [
            "FPF < 5 µm'i, EFPF < ~2 µm'i kapsar — EFPF daha derin bölgeyi temsil eder.",
            "Küçük havayolu hastalığı (KOAH, şiddetli astım) için önemlidir.",
            "Çok düşük çap ekshalasyon kaybını artırabilir; denge gerekir.",
            "EFPF optimizasyonu MMAD'yi düşürmeyi ve dağılımı daraltmayı içerir.",
        ],
        "devices": {
            "neb": "Mesh teknolojisi ince fraksiyonu artırabilir.",
            "pmdi": "Ekstra ince solüsyon pMDI'lar (örn. küçük partikül) yüksek EFPF sağlar.",
            "dpi": "Partikül mühendisliği ile EFPF artırılabilir.",
        },
        "widget": "lung",
    },
    {
        "id": "rf",
        "title": "6. RF (Solunabilir Fraksiyon)",
        "lead": (
            "RF, terapötik açıdan en etkili kabul edilen 1–5 µm aralığındaki "
            "partiküllerin oranıdır. Bronşiyal ve bronşiyolar bölgeye etkin "
            "iletim ile ilişkilidir."
        ),
        "points": [
            "RF ≈ 1–5 µm aralığı kütle fraksiyonu.",
            "MMAD optimal pencerede (2–4 µm) ise RF yüksektir.",
            "Yüksek GSD, RF dışına taşan iri/ince partikülleri artırır.",
            "RF, MMAD ve GSD'nin birleşik sonucudur.",
        ],
        "devices": {
            "neb": "Viskozite ve mesh ayarı RF'yi belirler.",
            "pmdi": "Orifis ve propellant ayarı RF penceresini etkiler.",
            "dpi": "Akış hızı RF'yi güçlü etkiler.",
        },
        "widget": "lung",
    },
    {
        "id": "apsd",
        "title": "7. APSD (Aerodinamik Partikül Boyut Dağılımı)",
        "lead": (
            "APSD, aerosoldeki ilacın aerodinamik çapa göre kütle dağılımının "
            "tam profilidir. NGI ile kademe kademe ölçülür ve tüm türetilmiş "
            "parametrelerin (MMAD, GSD, FPF, RF) kaynağıdır."
        ),
        "points": [
            "NGI her kademede belirli kesim çapının üzerindeki partikülleri toplar.",
            "Kademe kütleleri kümülatif dağılıma dönüştürülür.",
            "APSD profili formülasyon ve cihaz değişikliklerine duyarlıdır.",
            "Düzenleyici başvurularda tam APSD profili istenir.",
        ],
        "devices": {
            "neb": "15 L/dk kurulum; süspansiyonlarda özel dikkat.",
            "pmdi": "28.3 L/dk; spacer ile profil değişir.",
            "dpi": "60 L/dk (4 kPa); profil akışa bağımlı raporlanır.",
        },
        "widget": "ngi",
    },
    {
        "id": "cmd",
        "title": "8. Kümülatif Kütle Dağılımı (CMD)",
        "lead": (
            "CMD, belirli bir çapın altındaki kümülatif kütle yüzdesini "
            "gösterir. Log-olasılık grafiğinde %50 kesişimi MMAD'yi, eğim ise "
            "GSD'yi verir."
        ),
        "points": [
            "CMD = kademe kütlelerinin küçükten büyüğe kümülatif toplamı.",
            "Log-olasılık kağıdında doğrusal eğri log-normalliği gösterir.",
            "d₅₀ → MMAD; d₈₄.₁/d₅₀ → GSD.",
            "Eğride kırılma bimodal dağılıma işaret eder.",
            "Kütle dengesi (total recovery) CMD güvenilirliğini belirler.",
        ],
        "devices": {
            "neb": "Süspansiyonlarda bimodalite görülebilir.",
            "pmdi": "Genelde tek modlu, dar CMD.",
            "dpi": "Taşıyıcı-API ayrışması CMD şeklini etkiler.",
        },
        "widget": "cmd",
    },
    {
        "id": "recovery",
        "title": "9. NGI Toplam Geri Kazanım",
        "lead": (
            "Total Recovery, tüm NGI bileşenlerinden geri kazanılan ilaç "
            "miktarının etikette belirtilen doza oranıdır. Ölçümün geçerliliği "
            "için temel kabul kriteridir."
        ),
        "points": [
            "Kabul aralığı tipik olarak etiket dozunun %85–115'i.",
            "Düşük recovery: kayıp, adsorpsiyon, eksik yıkama, buharlaşma.",
            "Yüksek recovery: kontaminasyon, kalibrasyon/seyreltme hatası.",
            "Recovery dışıysa APSD verisi geçersiz sayılır.",
        ],
        "devices": {
            "neb": "Uzun nebülizasyonda buharlaşma kaybına dikkat.",
            "pmdi": "Aktüatör/valf ölü hacmi recovery'i etkiler.",
            "dpi": "Cihazda kalan toz (device retention) hesaba katılır.",
        },
        "widget": None,
    },
    {
        "id": "stage",
        "title": "10. NGI Stage Deposizyon Profili (1–7)",
        "lead": (
            "Stage profili, ilacın NGI kademelerine (kesim çaplarına göre) "
            "nasıl dağıldığını gösterir. Profilin şekli MMAD ve GSD'yi doğrudan "
            "yansıtır."
        ),
        "points": [
            "Her kademenin 60 L/dk'da nominal kesim çapı vardır (S1≈8.06 µm … S7≈0.34 µm).",
            "MOC en ince partikülleri toplar.",
            "Profilin tepe noktası baskın partikül boyutunu gösterir.",
            "İnce kademelere kayan profil daha derin deposizyon demektir.",
        ],
        "devices": {
            "neb": "Profil genelde orta kademelerde yayılır.",
            "pmdi": "Daha dar, tek tepeli profil.",
            "dpi": "Akış arttıkça profil ince kademelere kayar.",
        },
        "widget": "ngi",
    },
    {
        "id": "ip",
        "title": "11. İndüksiyon Port Deposizyonu",
        "lead": (
            "İndüksiyon Port (IP), ağız-boğaz bölgesinin anatomik karşılığıdır. "
            "Buradaki yüksek deposizyon, ilacın boşa gitmesi ve lokal yan etki "
            "anlamına gelir."
        ),
        "points": [
            "IP deposizyonu akciğere ulaşmayan kaybı temsil eder.",
            "Yüksek hızlı/iri partiküller IP'de inertial impaction ile çöker.",
            "Azaltma: daha küçük MMAD, daha düşük püskürtme hızı, spacer.",
            "IP kütlesi FPD hesabından dışlanır.",
        ],
        "devices": {
            "neb": "IP kaybı genelde düşüktür (düşük hız).",
            "pmdi": "Yüksek sprey hızı IP kaybını artırır; spacer azaltır.",
            "dpi": "Yüksek akış IP impaksiyonunu artırabilir.",
        },
        "widget": None,
    },
    {
        "id": "preseparator",
        "title": "12. Pre-Separatör Deposizyonu",
        "lead": (
            "Pre-separatör, NGI öncesinde çok iri partikülleri ve süspansiyon "
            "damlacıklarını tutarak kademelerin aşırı yüklenmesini ve "
            "buharlaşma artefaktını önler."
        ),
        "points": [
            "Özellikle süspansiyon ve nebülizer ürünlerde kullanılır.",
            "İri damlacıkların kademelere taşınmasını engeller.",
            "Pre-separatör kütlesi de FPD'den dışlanır.",
            "Aşırı pre-separatör deposizyonu iri APSD'ye işaret eder.",
        ],
        "devices": {
            "neb": "Sıvı damlacıklar için kritik; sıklıkla zorunlu.",
            "pmdi": "Süspansiyon pMDI'larda gerekebilir.",
            "dpi": "Genelde iri taşıyıcı (laktoz) partiküllerini tutar.",
        },
        "widget": None,
    },
    {
        "id": "quality",
        "title": "13. Kalite Sistemi ve Regülatör Çerçeve",
        "lead": (
            "APSD parametreleri, Kritik Kalite Özellikleri (CQA) olarak QbD ve "
            "ICH Q8–Q10 çerçevesinde yönetilir. Ph. Eur. 2.9.18, USP <601>, "
            "EMA OIP ve FDA OIP kılavuzları temel referanslardır."
        ),
        "points": [
            "MMAD, GSD, FPF/FPD ve total recovery temel CQA'lardır.",
            "Ölçüm koşulları validasyon raporunda açıkça tanımlanır.",
            "Biyoeşdeğerlikte referans ile MMAD + GSD + profil eşleşmesi beklenir.",
            "Tasarım uzayı (ICH Q8) parametre limitlerini belirler.",
        ],
        "devices": {
            "neb": "EMA nebülizer kılavuzu özel akış/hacim koşulları tanımlar.",
            "pmdi": "Doz tekdüzeliği ve sprey paterni ek CQA'lardır.",
            "dpi": "Akışa bağlı performans çoklu hızda raporlanır.",
        },
        "widget": "relationship",
    },
    {
        "id": "conclusion",
        "title": "14. Sonuç ve Öneriler",
        "lead": (
            "Aerodinamik karakterizasyon, inhaler ürün geliştirmenin merkezindedir. "
            "MMAD ve GSD birlikte deposizyon profilini şekillendirir; FPF, FPD, "
            "RF ve EFPF bu profilin klinik anlamını taşır."
        ),
        "points": [
            "Tek bir parametre yeterli değildir; profil bütüncül yorumlanır.",
            "Cihaz tipi (neb/pMDI/DPI) hedef profili ve test koşulunu belirler.",
            "QbD yaklaşımı ile CQA'lar tasarım uzayı içinde kontrol edilir.",
            "Bu programdaki simülasyonlarla parametre-deposizyon ilişkisini "
            "deneyerek pekiştirin.",
        ],
        "devices": {
            "neb": "Düşük efor, geniş hasta grubu; profil orta kademelerde.",
            "pmdi": "Dar profil, koordinasyon/spacer kritik.",
            "dpi": "Akışa bağımlı; çoklu hız değerlendirmesi şart.",
        },
        "widget": "relationship",
    },
]
