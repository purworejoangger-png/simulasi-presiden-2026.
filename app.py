import os
import random
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "kunci-rahasia-istana-negara-2026")

# Data Kebijakan Reguler Kondisi Indonesia 2026
KEBIJAKAN = [
    {
        "id": "mbg",
        "nama": "Akselerasi Makan Bergizi Gratis (MBG)",
        "deskripsi": "Perluas dapur SPPG ke seluruh pelosok untuk 80 juta penerima manfaat.",
        "biaya": "Rp 350 Triliun (APBN Unlimited)",
        "efek": {"rakyat": 12, "ekonomi": 5, "stabilitas": 4, "lingkungan": -2},
        "berita": "Program MBG menjangkau jutaan siswa baru; UMKM katering daerah kebanjiran order."
    },
    {
        "id": "pangan_energi",
        "nama": "Swasembada Pangan & Mandatori Biodiesel B50",
        "deskripsi": "Cetak sawah baru, serap gabah via Bulog, dan terapkan penuh bahan bakar B50.",
        "biaya": "Rp 210 Triliun (APBN Unlimited)",
        "efek": {"rakyat": 6, "ekonomi": 10, "stabilitas": 5, "lingkungan": -5},
        "berita": "Impor beras & solar turun drastis! Indonesia resmi menuju kemandirian pangan & energi."
    },
    {
        "id": "danantara",
        "nama": "Suntik Modal Superholding Danantara & Hilirisasi",
        "deskripsi": "Biayai proyek strategis nasional dan industri hilirisasi nikel, bauksit, serta baterai EV.",
        "biaya": "Rp 500 Triliun (APBN Unlimited)",
        "efek": {"rakyat": 2, "ekonomi": 15, "stabilitas": 3, "lingkungan": -8},
        "berita": "Investasi industri hilir melonjak tajam, IHSG menguat, namun aktivis lingkungan menyoroti tambang."
    },
    {
        "id": "subsidi_tepat",
        "nama": "Reformasi Subsidi Energi & Bantuan Tunai Kelas Menengah",
        "deskripsi": "Alihkan subsidi BBM ke bantuan langsung digital & insentif daya beli pekerja.",
        "biaya": "Rp 180 Triliun (APBN Unlimited)",
        "efek": {"rakyat": 9, "ekonomi": 7, "stabilitas": -4, "lingkungan": 4},
        "berita": "Daya beli kelas menengah kembali pulih, meski sempat memicu perdebatan hangat di parlemen."
    },
    {
        "id": "karhutla_ikn",
        "nama": "Operasi Modifikasi Cuaca (OMC) & Pemulihan Ekologi",
        "deskripsi": "Kerahkan armada udara padamkan Karhutla di Sumatera-Kalimantan dan reboisasi besar-besaran.",
        "biaya": "Rp 95 Triliun (APBN Unlimited)",
        "efek": {"rakyat": 5, "ekonomi": -2, "stabilitas": 4, "lingkungan": 16},
        "berita": "Titik panas (hotspot) Karhutla turun 80%, kualitas udara membaik dan mendapat apresiasi global."
    },
    {
        "id": "konsolidasi",
        "nama": "Konsolidasi Politik & Reformasi Birokrasi Digital",
        "deskripsi": "Perkuat koordinasi Kabinet Merah Putih, digitalisasi layanan publik, dan berantas pungli.",
        "biaya": "Rp 75 Triliun (APBN Unlimited)",
        "efek": {"rakyat": 7, "ekonomi": 6, "stabilitas": 14, "lingkungan": 2},
        "berita": "Kepastian hukum meningkat! Investor asing kembali mencatatkan net inflow ke pasar domestik."
    }
]

# Skenario Dilema Krisis (Popup Pilihan A vs B)
KRISIS_DILEMA = [
    {
        "id": "krisis_karhutla",
        "kategori": "DARURAT EKOLOGI & BENCANA",
        "judul": "Kabut Asap Karhutla Meluas di Sumatera & Kalimantan!",
        "deskripsi": "Musim kemarau ekstrem memicu ratusan titik api di lahan konsesi perkebunan dan gambut. Aktivitas penerbangan terganggu dan negara tetangga mulai melayangkan protes diplomatik.",
        "opsi_a": {
            "label": "Opsi A: Cabut Izin Korporasi Pembakar Lahan & Kerahkan Satgas TNI/Polri",
            "dampak_teks": "Rakyat & Ekologi puas, namun lobi pengusaha besar menggoyang stabilitas politik.",
            "efek": {"rakyat": 8, "ekonomi": -6, "stabilitas": -9, "lingkungan": 14},
            "berita": "Presiden bertindak tegas mencabut izin konsesi pembakar hutan; kabut asap mulai terkendali."
        },
        "opsi_b": {
            "label": "Opsi B: Kucurkan Dana Kompensasi Pemulihan ke Pengusaha & Fokus Hujan Buatan",
            "dampak_teks": "Ekonomi & koalisi aman, tetapi aktivis lingkungan dan warga terdampak kecewa.",
            "efek": {"rakyat": -7, "ekonomi": 4, "stabilitas": 6, "lingkungan": -5},
            "berita": "Pemerintah memilih pendekatan persuasif dan modifikasi cuaca tanpa sanksi pencabutan izin."
        }
    },
    {
        "id": "krisis_politik",
        "kategori": "GEJOLAK POLITIK & KOALISI",
        "judul": "Ketegangan di Parlemen Soal Revisi UU & Jatah Kursi Strategis",
        "deskripsi": "Sejumlah partai koalisi mengancam memboikot pengesahan program prioritas pemerintah jika tuntutan politik mereka tidak diakomodasi dalam waktu 48 jam.",
        "opsi_a": {
            "label": "Opsi A: Akomodasi Tuntutan Koalisi & Tambah Kursi Wamen",
            "dampak_teks": "Stabilitas parlemen terkunci aman, namun publik mengkritik gemuknya birokrasi.",
            "efek": {"rakyat": -9, "ekonomi": 2, "stabilitas": 15, "lingkungan": 0},
            "berita": "Kompromi politik tercapai di Istana; koalisi kembali solid namun menuai kritik pengamat."
        },
        "opsi_b": {
            "label": "Opsi B: Tolak Tekanan & Gelar Pidato Terbuka ke Rakyat",
            "dampak_teks": "Popularitas di mata rakyat meroket, namun manuver oposisi di DPR makin liar.",
            "efek": {"rakyat": 12, "ekonomi": -3, "stabilitas": -12, "lingkungan": 0},
            "berita": "Presiden menolak tunduk pada tekanan elite; dukungan publik mengalir deras di media sosial."
        }
    },
    {
        "id": "krisis_pangan",
        "kategori": "GEJOLAK HARGA & LOGISTIK PANGAN",
        "judul": "Anomali Cuaca Hambat Panen, Harga Beras & Cabai Melonjak!",
        "deskripsi": "Gangguan distribusi akibat cuaca ekstrem membuat harga pangan pokok naik 25% di pasar tradisional menjelang hari besar keagamaan.",
        "opsi_a": {
            "label": "Opsi A: Buka Keran Impor Darurat & Banjiri Pasar dengan Operasi Murah",
            "dampak_teks": "Harga langsung turun dan rakyat senang, tetapi petani lokal memprotes anjloknya harga gabah.",
            "efek": {"rakyat": 10, "ekonomi": -4, "stabilitas": -5, "lingkungan": 0},
            "berita": "Operasi pasar masif berhasil meredam inflasi pangan dalam sepekan."
        },
        "opsi_b": {
            "label": "Opsi B: Pertahankan Larangan Impor & Beri BLT Pangan Tunai",
            "dampak_teks": "Petani dan ekonomi domestik terlindungi, namun kelas menengah mengeluhkan harga pasar.",
            "efek": {"rakyat": -4, "ekonomi": 6, "stabilitas": 5, "lingkungan": 0},
            "berita": "Pemerintah menolak impor demi melindungi petani dan menyalurkan BLT pangan ke warga rentan."
        }
    },
    {
        "id": "krisis_rupiah",
        "kategori": "TEKANAN EKONOMI GLOBAL",
        "judul": "Arus Modal Asing Keluar, Nilai Tukar Rupiah Tertekan!",
        "deskripsi": "Ketegangan geopolitik global memicu penguatan Dolar AS. Importir bahan baku industri mulai menjerit akibat lonjakan biaya produksi.",
        "opsi_a": {
            "label": "Opsi A: Wajibkan Devisa Hasil Ekspor (DHE) 100% Parkir di Bank Dalam Negeri",
            "dampak_teks": "Rupiah langsung menguat tajam, namun eksportir mengeluhkan ketatnya likuiditas.",
            "efek": {"rakyat": 4, "ekonomi": 9, "stabilitas": -6, "lingkungan": 0},
            "berita": "Kebijakan DHE ketat sukses menstabilkan Rupiah di tengah badai finansial global."
        },
        "opsi_b": {
            "label": "Opsi B: Berikan Insentif Pajak & Subsidi Bunga Kredit untuk Eksportir",
            "dampak_teks": "Dunia usaha dan investor menyambut positif, namun efek penguatan Rupiah berjalan lambat.",
            "efek": {"rakyat": -5, "ekonomi": 5, "stabilitas": 7, "lingkungan": -2},
            "berita": "Paket stimulus ekspor diluncurkan untuk menjaga daya saing industri nasional."
        }
    }
]

EVENT_BIASA = [
    "Konsumsi domestik dan transaksi QRIS nasional tumbuh positif di kisaran 5,45%.",
    "Kunjungan kerja Presiden ke daerah disambut antusias warga dan pelaku UMKM.",
    "Realisasi investasi proyek hilirisasi berjalan sesuai jadwal kuartalan.",
    "Kinerja ekspor komoditas unggulan Indonesia mencatatkan surplus neraca dagang."
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulasi Presiden RI 2026 - Unlimited APBN</title>
    <style>
        :root {
            --merah: #ce1126;
            --merah-gelap: #9e0b1b;
            --emas: #d4af37;
            --bg: #0f172a;
            --card: #1e293b;
            --text: #f8fafc;
            --muted: #94a3b8;
        }
        * { box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        body {
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
        }
        .container { max-width: 920px; width: 100%; }
        .header {
            background: linear-gradient(135deg, var(--merah), #450a0a);
            padding: 24px;
            border-radius: 16px;
            border: 1px solid var(--emas);
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        .header h1 { margin: 0; font-size: 1.45rem; }
        .badge-unlimited {
            background: var(--emas);
            color: #000;
            font-weight: 800;
            padding: 8px 14px;
            border-radius: 999px;
            font-size: 0.9rem;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: var(--card);
            padding: 16px;
            border-radius: 12px;
            border: 1px solid #334155;
        }
        .stat-title { color: var(--muted); font-size: 0.85rem; margin-bottom: 6px; }
        .stat-val { font-size: 1.6rem; font-weight: bold; }
        .bar-bg { background: #334155; height: 8px; border-radius: 4px; margin-top: 8px; overflow: hidden; }
        .bar-fill { height: 100%; transition: width 0.3s; }
        .news-box {
            background: #172033;
            border-left: 4px solid var(--emas);
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .news-box h3 { margin: 0 0 8px 0; color: var(--emas); font-size: 1rem; }
        .policies-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
            gap: 15px;
        }
        .policy-card {
            background: var(--card);
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #334155;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .policy-card h4 { margin: 0 0 8px 0; font-size: 1.05rem; }
        .policy-card p { color: var(--muted); font-size: 0.88rem; margin: 0 0 12px 0; line-height: 1.4; }
        .cost { color: #4ade80; font-size: 0.8rem; font-weight: bold; margin-bottom: 12px; }
        button {
            background: var(--merah);
            color: white;
            border: none;
            padding: 10px 14px;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            transition: background 0.2s;
        }
        button:hover { background: var(--merah-gelap); }
        .btn-reset { background: #334155; width: auto; padding: 8px 16px; }
        .btn-reset:hover { background: #475569; }
        .gameover {
            background: #450a0a;
            border: 2px solid #ef4444;
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Styling Modal Popup Dilema Krisis */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(2, 6, 23, 0.86);
            backdrop-filter: blur(5px);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            z-index: 999;
        }
        .modal-box {
            background: #1e293b;
            border: 2px solid #ef4444;
            border-radius: 16px;
            max-width: 620px;
            width: 100%;
            padding: 26px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.75);
            animation: popIn 0.25s ease-out;
        }
        @keyframes popIn {
            from { transform: scale(0.92); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        .crisis-badge {
            display: inline-block;
            background: #ef4444;
            color: #fff;
            font-size: 0.75rem;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 6px;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }
        .modal-box h2 { margin: 0 0 10px 0; font-size: 1.35rem; color: #f8fafc; }
        .modal-box p.desc { color: #cbd5e1; line-height: 1.5; margin-bottom: 20px; font-size: 0.95rem; }
        .choice-card {
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 14px;
        }
        .choice-card small {
            display: block;
            color: #94a3b8;
            margin-bottom: 10px;
            font-size: 0.85rem;
        }
        .btn-opsi-a { background: #dc2626; }
        .btn-opsi-a:hover { background: #b91c1c; }
        .btn-opsi-b { background: #2563eb; }
        .btn-opsi-b:hover { background: #1d4ed8; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div>
            <h1>🇮🇩 Simulasi Presiden RI — Kabinet Merah Putih (2026)</h1>
            <div style="color: #fca5a5; font-size: 0.9rem; margin-top: 4px;">
                Periode: <strong>Kuartal {{ state.kuartal }} / Tahun {{ state.tahun }}</strong>
            </div>
        </div>
        <div style="display:flex; gap:10px; align-items:center;">
            <span class="badge-unlimited">APBN: ∞ UNLIMITED</span>
            <form method="POST" action="/reset" style="margin:0;">
                <button type="submit" class="btn-reset">Reset Game</button>
            </form>
        </div>
    </div>

    {% if state.game_over %}
    <div class="gameover">
        <h2>⚠️ PEMERINTAHAN BERAKHIR LEBIH AWAL</h2>
        <p>{{ state.alasan_kalah }}</p>
        <form method="POST" action="/reset">
            <button type="submit" style="max-width:220px;">Mulai Periode Baru</button>
        </form>
    </div>
    {% endif %}

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-title">Kepuasan Rakyat</div>
            <div class="stat-val">{{ state.rakyat }}%</div>
            <div class="bar-bg"><div class="bar-fill" style="width:{{ state.rakyat }}%; background:#38bdf8;"></div></div>
        </div>
        <div class="stat-card">
            <div class="stat-title">Pertumbuhan Ekonomi</div>
            <div class="stat-val">{{ "%.2f"|format(state.pertumbuhan_ekonomi) }}%</div>
            <div class="bar-bg"><div class="bar-fill" style="width:{{ state.ekonomi }}%; background:#4ade80;"></div></div>
        </div>
        <div class="stat-card">
            <div class="stat-title">Stabilitas Politik & Koalisi</div>
            <div class="stat-val">{{ state.stabilitas }}%</div>
            <div class="bar-bg"><div class="bar-fill" style="width:{{ state.stabilitas }}%; background:#facc15;"></div></div>
        </div>
        <div class="stat-card">
            <div class="stat-title">Ketahanan Ekologi & Iklim</div>
            <div class="stat-val">{{ state.lingkungan }}%</div>
            <div class="bar-bg"><div class="bar-fill" style="width:{{ state.lingkungan }}%; background:#34d399;"></div></div>
        </div>
    </div>

    <div class="news-box">
        <h3>📰 Breaking News Istana Negara</h3>
        <p style="margin:0 0 6px 0;"><strong>Keputusan Terakhir:</strong> {{ state.berita_kebijakan }}</p>
        <p style="margin:0; color:#cbd5e1;"><strong>Laporan Situasi:</strong> {{ state.berita_event }}</p>
    </div>

    {% if not state.game_over %}
    <h3 style="margin-bottom: 12px;">Pilih Keputusan Strategis Kuartal Ini:</h3>
    <div class="policies-grid">
        {% for item in kebijakan %}
        <div class="policy-card">
            <div>
                <h4>{{ item.nama }}</h4>
                <p>{{ item.deskripsi }}</p>
            </div>
            <div>
                <div class="cost">Anggaran: {{ item.biaya }}</div>
                <form method="POST" action="/aksi">
                    <input type="hidden" name="kebijakan_id" value="{{ item.id }}">
                    <button type="submit">Sahkan Keppres</button>
                </form>
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}
</div>

<!-- POPUP MODAL DILEMA KRISIS -->
{% if krisis_aktif and not state.game_over %}
<div class="modal-overlay">
    <div class="modal-box">
        <span class="crisis-badge">🚨 {{ krisis_aktif.kategori }}</span>
        <h2>{{ krisis_aktif.judul }}</h2>
        <p class="desc">{{ krisis_aktif.deskripsi }}</p>

        <div class="choice-card">
            <small>💡 {{ krisis_aktif.opsi_a.dampak_teks }}</small>
            <form method="POST" action="/jawab_krisis">
                <input type="hidden" name="pilihan" value="a">
                <button type="submit" class="btn-opsi-a">{{ krisis_aktif.opsi_a.label }}</button>
            </form>
        </div>

        <div class="choice-card" style="margin-bottom:0;">
            <small>💡 {{ krisis_aktif.opsi_b.dampak_teks }}</small>
            <form method="POST" action="/jawab_krisis">
                <input type="hidden" name="pilihan" value="b">
                <button type="submit" class="btn-opsi-b">{{ krisis_aktif.opsi_b.label }}</button>
            </form>
        </div>
    </div>
</div>
{% endif %}

</body>
</html>
"""

def init_state():
    return {
        "tahun": 2026,
        "kuartal": 4,
        "rakyat": 62,
        "ekonomi": 55,
        "stabilitas": 58,
        "lingkungan": 50,
        "berita_kebijakan": "Anda memimpin rapat paripurna Kabinet Merah Putih di akhir tahun 2026 dengan kas negara tak terbatas.",
        "berita_event": "Pertumbuhan ekonomi RI tercatat di kisaran 5,45%. Waspadai potensi krisis politik maupun cuaca ekstrem.",
        "krisis_id": None,
        "game_over": False,
        "alasan_kalah": ""
    }

def clamp(val):
    return max(0, min(100, val))

def cek_game_over(state):
    if state["rakyat"] <= 10:
        state["game_over"] = True
        state["alasan_kalah"] = "Gelombang demonstrasi nasional tak terbendung akibat tingkat kepuasan rakyat di bawah 10%."
    elif state["stabilitas"] <= 10:
        state["game_over"] = True
        state["alasan_kalah"] = "Krisis politik dan mosi tidak percaya di parlemen melumpuhkan pemerintahan."
    elif state["lingkungan"] <= 10:
        state["game_over"] = True
        state["alasan_kalah"] = "Darurat bencana ekologis dan kabut asap nasional melumpuhkan aktivitas negara."

@app.route("/")
def index():
    if "state" not in session:
        session["state"] = init_state()
    state = session["state"]
    state["pertumbuhan_ekonomi"] = round(2.0 + (state["ekonomi"] / 100.0) * 6.5, 2)

    krisis_aktif = None
    if state.get("krisis_id"):
        krisis_aktif = next((k for k in KRISIS_DILEMA if k["id"] == state["krisis_id"]), None)

    return render_template_string(
        HTML_TEMPLATE,
        state=state,
        kebijakan=KEBIJAKAN,
        krisis_aktif=krisis_aktif
    )

@app.route("/aksi", methods=["POST"])
def aksi():
    if "state" not in session:
        session["state"] = init_state()
    state = session["state"]

    # Blokir aksi reguler jika sedang ada krisis yang belum dijawab
    if state["game_over"] or state.get("krisis_id"):
        return redirect(url_for("index"))

    kebijakan_id = request.form.get("kebijakan_id")
    pilihan = next((k for k in KEBIJAKAN if k["id"] == kebijakan_id), None)

    if pilihan:
        state["rakyat"] = clamp(state["rakyat"] + pilihan["efek"]["rakyat"])
        state["ekonomi"] = clamp(state["ekonomi"] + pilihan["efek"]["ekonomi"])
        state["stabilitas"] = clamp(state["stabilitas"] + pilihan["efek"]["stabilitas"])
        state["lingkungan"] = clamp(state["lingkungan"] + pilihan["efek"]["lingkungan"])
        state["berita_kebijakan"] = pilihan["berita"]

        # Majukan waktu 1 kuartal
        state["kuartal"] += 1
        if state["kuartal"] > 4:
            state["kuartal"] = 1
            state["tahun"] += 1

        # 55% peluang muncul Popup Dilema Krisis
        if random.random() < 0.55:
            krisis = random.choice(KRISIS_DILEMA)
            state["krisis_id"] = krisis["id"]
            state["berita_event"] = f"DARURAT: {krisis['judul']} Menunggu keputusan langsung Presiden!"
        else:
            state["berita_event"] = random.choice(EVENT_BIASA)

        cek_game_over(state)
        session["state"] = state

    return redirect(url_for("index"))

@app.route("/jawab_krisis", methods=["POST"])
def jawab_krisis():
    if "state" not in session:
        session["state"] = init_state()
    state = session["state"]

    krisis_id = state.get("krisis_id")
    if not krisis_id or state["game_over"]:
        return redirect(url_for("index"))

    krisis = next((k for k in KRISIS_DILEMA if k["id"] == krisis_id), None)
    pilihan_opsi = request.form.get("pilihan")

    if krisis and pilihan_opsi in ("a", "b"):
        opsi = krisis["opsi_a"] if pilihan_opsi == "a" else krisis["opsi_b"]
        state["rakyat"] = clamp(state["rakyat"] + opsi["efek"]["rakyat"])
        state["ekonomi"] = clamp(state["ekonomi"] + opsi["efek"]["ekonomi"])
        state["stabilitas"] = clamp(state["stabilitas"] + opsi["efek"]["stabilitas"])
        state["lingkungan"] = clamp(state["lingkungan"] + opsi["efek"]["lingkungan"])
        state["berita_event"] = opsi["berita"]
        state["krisis_id"] = None

        cek_game_over(state)
        session["state"] = state

    return redirect(url_for("index"))

@app.route("/reset", methods=["POST"])
def reset():
    session["state"] = init_state()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
