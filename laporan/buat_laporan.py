"""
Pembuat laporan otomatis (laporan/Laporan_fplib.docx -> PDF).

Isi teknis (kode fungsi, matriks, file & baris pemanggilan, hasil pytest)
diambil LANGSUNG dari kode saat skrip dijalankan, sehingga laporan selalu
sesuai dengan repositori.

Pemakaian (dari folder utama repo):
    pip install -r laporan/requirements-laporan.txt
    python laporan/buat_laporan.py
Lalu buka Laporan_fplib.docx di Word -> File -> Save As -> PDF,
atau (jika LibreOffice terpasang):
    soffice --headless --convert-to pdf --outdir laporan laporan/Laporan_fplib.docx

Isi bagian bertanda [ ... ] (nama, NIM, dosen, URL repo) di IDENTITAS di bawah.
"""

import ast
import re
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

AKAR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKAR / "tools"))
import matriks  # noqa: E402  (tools/matriks.py)

# ---------------------------------------------------------------------------
# IDENTITAS — isi sebelum dikumpulkan
# ---------------------------------------------------------------------------
IDENTITAS = {
    "kelas": "Pemrograman Fungsional G",
    "dosen": "Irtafa Masyuri, S.S.T., M.Tr.T.",
    "repo": "https://github.com/baybayyy26/fplib-pemrograman-fungsional",
    "anggota": [
        ("Aditiya Al Bayhaqy", "202410370110502",
         "fplib.py, test_fplib.py, Kasir Kantin, Presensi Kelas, README & repositori"),
        ("Sigit Novriyanto", "202410370110500",
         "Perpustakaan Mini, Keuangan Pribadi, Nilai Mahasiswa, laporan"),
    ],
}

FONT = "Times New Roman"
FONT_KODE = "Consolas"
WARNA_AKSEN = RGBColor(0, 0, 0)  # judul hitam, format laporan formal
LEBAR_TEKS = 14.0  # A4 21 cm - margin kiri 4 cm - kanan 3 cm
SPASI = 1.5
WARNA_KEPALA_TABEL = "DCE8DF"

PENJELASAN = {
    "pipe": (
        "Merangkai beberapa fungsi menjadi satu alur yang dijalankan dari kiri ke kanan, sehingga "
        "`pipe(f, g, h)(data)` sama dengan `h(g(f(data)))`. Tanpa langkah, `pipe()` menghasilkan fungsi "
        "yang mengembalikan data apa adanya.",
        "Fungsi ini memakai `reduce` dari modul `functools` [2]. Proses dimulai dari data, lalu setiap "
        "fungsi di dalam `langkah` menerima hasil fungsi sebelumnya.",
    ),
    "ambil": (
        "Mengubah setiap elemen data, seperti `map`. Pemanggilan `ambil(\"nama\")` menghasilkan daftar nilai "
        "satu kolom, `ambil(\"nama\", \"nilai\")` menghasilkan daftar dict berisi kolom tersebut, dan "
        "`ambil(fungsi)` menerapkan fungsi ke setiap elemen.",
        "Kunci diubah menjadi fungsi pengubah, lalu dijalankan dengan `map` dan hasilnya dibungkus `list`. "
        "Di aplikasi, `ambil` juga dipakai untuk mengubah setiap data menjadi satu baris teks tampilan.",
    ),
    "saring": (
        "Memilih elemen yang memenuhi syarat (predikat), seperti `filter`.",
        "Fungsi ini membungkus `filter` bawaan Python [3] dan mengubah hasilnya menjadi list baru, "
        "sehingga data asli tidak berubah.",
    ),
    "cari": (
        "Mengembalikan elemen pertama yang memenuhi syarat, atau nilai bawaan (`None`) jika tidak ada.",
        "Fungsi ini memakai `next(filter(predikat, data), bawaan)`. Karena `filter` bersifat malas (lazy), "
        "pencarian berhenti begitu elemen pertama ditemukan; jika tidak ada, `next` mengembalikan nilai "
        "bawaan tanpa galat [3].",
    ),
    "urutkan": (
        "Mengurutkan data berdasarkan kunci, menaik atau menurun, tanpa mengubah data asli.",
        "Fungsi ini memakai `sorted`, yang membuat list baru (berbeda dengan `list.sort` yang mengubah list "
        "asli). Pengurutannya stabil [4]; untuk urutan bertingkat, kunci berupa fungsi yang menghasilkan tuple.",
    ),
    "kelompokkan": (
        "Mengelompokkan data menjadi dict berbentuk kunci dan daftar elemen, dengan urutan kemunculan tetap.",
        "Fungsi ini memakai `reduce` dengan dict kosong sebagai nilai awal. Setiap langkah membuat dict "
        "baru yang berisi kelompok lama ditambah elemen berikutnya, sehingga tidak ada struktur yang diubah. "
        "Berbeda dengan `itertools.groupby`, data tidak perlu diurutkan terlebih dahulu.",
    ),
    "jumlahkan": (
        "Menjumlahkan nilai setiap elemen. Fungsi ini mengikuti contoh di slide; yang berbeda antaraplikasi "
        "hanya fungsi nilai yang dikirim sebagai argumen.",
        "Rumusnya `sum(map(f, data))`, dengan `f` hasil `_ke_fungsi`: `map` menghitung nilai tiap elemen, "
        "lalu `sum` menjumlahkannya. Data kosong menghasilkan 0.",
    ),
    "rata_rata": (
        "Menghitung rata-rata nilai seluruh elemen; data kosong menghasilkan 0,0 tanpa galat.",
        "Nilai dihitung dengan `map`, lalu jumlahnya dibagi dengan banyaknya data. Di Presensi, rata-rata nilai 100 "
        "(hadir) atau 0 (tidak hadir) menjadi persentase kehadiran.",
    ),
    "validasi": (
        "Membuat pemeriksa data dari pasangan (syarat, pesan kesalahan). Pemeriksa menerima satu elemen "
        "dan mengembalikan daftar pesan kesalahan; daftar kosong berarti data valid.",
        "Aturan yang tidak lolos disaring dengan `filter`, lalu pesannya diambil dengan `map`. Syarat yang "
        "menimbulkan galat umum, seperti `KeyError` karena kolom tidak ada, dianggap gagal sehingga program tidak berhenti.",
    ),
    "rupiah": (
        "Memformat angka menjadi teks rupiah berpemisah titik, misalnya 1500000 menjadi Rp1.500.000.",
        "Angka dibulatkan setengah ke atas dengan `int(abs(angka) + 0.5)` karena `round()` memakai "
        "banker's rounding (2,5 menjadi 2). Karena menerima satu angka dan langsung mengembalikan teks, "
        "`rupiah` dapat dioper ke fungsi lain, misalnya `ambil(rupiah)`.",
    ),
}

APLIKASI_INFO = {
    "Kasir": ("Kasir Kantin", "kasir_kantin.py",
              "Menampilkan menu, menolak pesanan yang salah (jumlah 0 atau kode tidak ada), membentuk keranjang "
              "dengan `pipe`, `saring`, `ambil`, dan `urutkan`, lalu menghitung total belanja, uang yang dibayar, "
              "dan kembalian."),
    "Presensi": ("Presensi Kelas", "presensi_kelas.py",
                 "Mengelompokkan catatan kehadiran per mahasiswa dan per pertemuan, menghitung persentase "
                 "kehadiran dengan `rata_rata`, dan menyaring mahasiswa yang kehadirannya di bawah 75%."),
    "Perpus": ("Perpustakaan Mini", "perpustakaan_mini.py",
               "Menampilkan katalog per kategori beserta sisa stok, menghitung denda keterlambatan "
               "(batas 7 hari, Rp1.000 per hari), dan memvalidasi permintaan peminjaman baru."),
    "Keuangan": ("Keuangan Pribadi", "keuangan_pribadi.py",
                 "Memisahkan transaksi tidak valid, lalu menghitung pemasukan, pengeluaran, saldo, rekap "
                 "pengeluaran per kategori, dan rata-rata nominal pengeluaran."),
    "Nilai": ("Nilai Mahasiswa", "nilai_mahasiswa.py",
              "Memvalidasi komponen nilai, menghitung nilai akhir berbobot, menentukan nilai huruf dengan "
              "`cari`, menyusun peringkat, serta menghitung rata-rata kelas dan jumlah mahasiswa yang lulus."),
}

GAMBAR_APLIKASI = {
    "Kasir": "03_kasir_kantin.png",
    "Presensi": "04_presensi_kelas.png",
    "Perpus": "05_perpustakaan_mini.png",
    "Keuangan": "06_keuangan_pribadi.png",
    "Nilai": "07_nilai_mahasiswa.png",
}
LEBAR_GAMBAR_APLIKASI = 8.5
CM_PER_PX_KODE = 13.0 / 1047     # huruf kode sekitar 0,17 cm per karakter
CM_PER_PX_KELUARAN = 0.0160      # ukuran huruf keluaran setara dengan huruf kode
KETERANGAN_KELUARAN = {
    "Kasir": "pesanan ditolak, keranjang, dan total",
    "Presensi": "rekap kehadiran per mahasiswa",
    "Perpus": "denda keterlambatan dan permintaan pinjam",
    "Keuangan": "rekap pengeluaran dan saldo",
    "Nilai": "data tidak valid dan peringkat",
}


def lebar_gambar(nama_file, cm_per_px):
    """Lebar cetak (cm) sebanding dengan lebar piksel, supaya ukuran huruf di semua gambar sama."""
    from PIL import Image
    with Image.open(GAMBAR / nama_file) as im:
        return min(LEBAR_TEKS, im.width * cm_per_px)

PUSTAKA = [
    "Python Software Foundation. Functional Programming HOWTO. "
    "https://docs.python.org/3/howto/functional.html. Diakses 18 November 2026.",
    "Python Software Foundation. functools — Higher-order functions and operations on callable objects. "
    "https://docs.python.org/3/library/functools.html. Diakses 18 November 2026.",
    "Python Software Foundation. Built-in Functions. "
    "https://docs.python.org/3/library/functions.html. Diakses 18 November 2026.",
    "Python Software Foundation. Sorting Techniques. "
    "https://docs.python.org/3/howto/sorting.html. Diakses 18 November 2026.",
    "Python Software Foundation. ast — Abstract Syntax Trees. "
    "https://docs.python.org/3/library/ast.html. Diakses 18 November 2026.",
    "Python Software Foundation. venv — Creation of virtual environments. "
    "https://docs.python.org/3/library/venv.html. Diakses 18 November 2026.",
    "pytest-dev. pytest documentation. https://docs.pytest.org/. Diakses 18 November 2026.",
    "Python Software Foundation. The Python Tutorial: Modules. "
    "https://docs.python.org/3/tutorial/modules.html. Diakses 18 November 2026.",
]


# ---------------------------------------------------------------------------
# Pengambilan data dari repo
# ---------------------------------------------------------------------------
def sumber_fungsi():
    """{nama: (baris_awal, baris_akhir, kode_tanpa_docstring)} untuk fungsi di fplib.py."""
    teks = (AKAR / "fplib.py").read_text(encoding="utf-8")
    baris = teks.splitlines()
    hasil = {}
    for simpul in ast.parse(teks).body:
        if isinstance(simpul, ast.FunctionDef):
            awal, akhir = simpul.lineno, simpul.end_lineno
            buang = set()
            if (simpul.body and isinstance(simpul.body[0], ast.Expr)
                    and isinstance(simpul.body[0].value, ast.Constant)):
                buang = set(range(simpul.body[0].lineno, simpul.body[0].end_lineno + 1))
            # kode inti: baris def + pernyataan return tingkat atas (kode lengkap ada di repo)
            inti = [simpul.lineno] + [
                n for st in simpul.body if isinstance(st, ast.Return)
                for n in range(st.lineno, st.end_lineno + 1)
            ]
            kode = [f"{i:>3} | {baris[i - 1]}" for i in inti if i not in buang]
            hasil[simpul.name] = (awal, akhir, "\n".join(kode).rstrip())
    return hasil


def hasil_pytest():
    proses = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
        cwd=AKAR, capture_output=True, text=True,
    )
    keluaran = proses.stdout.strip().splitlines()
    ringkas = keluaran[-1].strip("= ") if keluaran else "pytest tidak berjalan"
    lulus = re.search(r"(\d+) passed", ringkas)
    gagal = re.search(r"(\d+) failed", ringkas)
    return ringkas, int(lulus.group(1)) if lulus else 0, int(gagal.group(1)) if gagal else 0


def keluaran_aplikasi(berkas, maks_baris=14):
    proses = subprocess.run([sys.executable, berkas], cwd=AKAR, capture_output=True, text=True)
    baris = proses.stdout.rstrip().splitlines()
    return baris[:maks_baris] + (["  ..."] if len(baris) > maks_baris else [])


# ---------------------------------------------------------------------------
# Pembantu format dokumen
# ---------------------------------------------------------------------------
def atur_font(run, ukuran=12, tebal=False, miring=False, nama=FONT, warna=None):
    run.font.name = nama
    run.font.size = Pt(ukuran)
    run.bold = tebal
    run.italic = miring
    run._element.rPr.rFonts.set(qn("w:eastAsia"), nama)
    if warna is not None:
        run.font.color.rgb = warna


def paragraf(doc, teks="", ukuran=12, tebal=False, miring=False, rata=WD_ALIGN_PARAGRAPH.JUSTIFY,
             sebelum=0, sesudah=6):
    p = doc.add_paragraph()
    p.alignment = rata
    p.paragraph_format.space_before = Pt(sebelum)
    p.paragraph_format.space_after = Pt(sesudah)
    p.paragraph_format.line_spacing = SPASI if rata == WD_ALIGN_PARAGRAPH.JUSTIFY else 1.15
    if rata == WD_ALIGN_PARAGRAPH.JUSTIFY:
        p.paragraph_format.first_line_indent = Cm(1.0)
    if teks:
        tambah_teks(p, teks, ukuran, tebal, miring)
    return p


def tambah_teks(p, teks, ukuran=12, tebal=False, miring=False):
    """Teks di antara `backtick` (nama fungsi, berkas, perintah) dicetak miring dengan huruf yang sama."""
    for i, bagian in enumerate(re.split(r"`([^`]*)`", teks)):
        if not bagian:
            continue
        run = p.add_run(bagian)
        if re.search(r"\[[A-Z][^\]]*\]", bagian):
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
        if i % 2:
            atur_font(run, ukuran, tebal, True)
        else:
            atur_font(run, ukuran, tebal, miring)


def judul(doc, teks, tingkat=1):
    h = doc.add_heading(level=tingkat)
    h.paragraph_format.space_before = Pt(12 if tingkat == 1 else 6)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(teks)
    atur_font(run, 12, tebal=True, warna=WARNA_AKSEN)
    return h


def poin(doc, teks):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    tambah_teks(p, teks)
    return p


def blok_kode(doc, kode, ukuran=9):
    tabel = doc.add_table(rows=1, cols=1)
    tabel.alignment = WD_TABLE_ALIGNMENT.CENTER
    sel = tabel.cell(0, 0)
    arsir(sel, "F3F5F4")
    sel.paragraphs[0].paragraph_format.space_after = Pt(0)
    for i, baris in enumerate(kode.splitlines()):
        p = sel.paragraphs[0] if i == 0 else sel.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(baris if baris else " ")
        atur_font(run, ukuran, nama=FONT_KODE)
    trPr = tabel.rows[0]._tr.get_or_add_trPr()
    tak_pecah = OxmlElement("w:cantSplit")
    tak_pecah.set(qn("w:val"), "true")
    trPr.append(tak_pecah)
    garis_tabel(tabel, "BFCFC4")
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def arsir(sel, warna):
    tcPr = sel._element.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), warna)
    tcPr.append(shd)


def garis_tabel(tabel, warna="8FA898"):
    tblPr = tabel._element.tblPr
    batas = OxmlElement("w:tblBorders")
    for sisi in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{sisi}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:color"), warna)
        batas.append(e)
    tblPr.append(batas)


def tabel(doc, kepala, isi, lebar_cm, ukuran=10, rata_tengah=(), utuh=False):
    if sum(lebar_cm) > LEBAR_TEKS:
        lebar_cm = [w * LEBAR_TEKS / sum(lebar_cm) for w in lebar_cm]
    t = doc.add_table(rows=1, cols=len(kepala))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, teks in enumerate(kepala):
        sel = t.rows[0].cells[i]
        arsir(sel, WARNA_KEPALA_TABEL)
        p = sel.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        tambah_teks(p, teks, ukuran, tebal=True)
    for baris in isi:
        sel_baris = t.add_row().cells
        for i, teks in enumerate(baris):
            p = sel_baris[i].paragraphs[0]
            if i in rata_tengah:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            tambah_teks(p, str(teks), ukuran)
    for i, kolom in enumerate(t.columns):
        kolom.width = Cm(lebar_cm[i])
    tblW = t._element.tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        t._element.tblPr.append(tblW)
    tblW.set(qn("w:w"), str(int(sum(lebar_cm) * 567)))
    tblW.set(qn("w:type"), "dxa")
    for baris in t.rows:
        for i, sel in enumerate(baris.cells):
            sel.width = Cm(lebar_cm[i])
            for p in sel.paragraphs:
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.space_before = Pt(1)
    for i, baris in enumerate(t.rows):
        trPr_b = baris._tr.get_or_add_trPr()
        tak_pecah = OxmlElement("w:cantSplit")
        tak_pecah.set(qn("w:val"), "true")
        trPr_b.append(tak_pecah)
        if utuh and i < len(t.rows) - 1:
            for sel in baris.cells:
                for p in sel.paragraphs:
                    p.paragraph_format.keep_with_next = True
    # ulangi kepala tabel di setiap halaman
    trPr = t.rows[0]._tr.get_or_add_trPr()
    ulang = OxmlElement("w:tblHeader")
    ulang.set(qn("w:val"), "true")
    trPr.append(ulang)
    garis_tabel(t)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


GAMBAR = AKAR / "laporan" / "gambar"
_nomor_gambar = [0]


def gambar(doc, nama_file, keterangan, lebar_cm=13.0, kecil=False):
    """Sisipkan screenshot asli (Google Colab / GitHub) beserta keterangan bernomor."""
    berkas = GAMBAR / nama_file
    if not berkas.exists():
        return
    _nomor_gambar[0] += 1
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(str(berkas), width=Cm(lebar_cm))
    k = paragraf(doc, "", 10, rata=WD_ALIGN_PARAGRAPH.CENTER, sesudah=4 if kecil else 8)
    tambah_teks(k, f"Gambar {_nomor_gambar[0]}. ", 10, tebal=True)
    tambah_teks(k, keterangan, 10, miring=True)


def gambar_grid(doc, daftar, lebar_cm=5.4):
    """Susun beberapa screenshot dalam tabel 2 kolom tanpa garis; tiap sel = gambar + keterangan."""
    baris = [daftar[i:i + 2] for i in range(0, len(daftar), 2)]
    t = doc.add_table(rows=len(baris), cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r, isi in enumerate(baris):
        trPr = t.rows[r]._tr.get_or_add_trPr()
        tak_pecah = OxmlElement("w:cantSplit")
        tak_pecah.set(qn("w:val"), "true")
        trPr.append(tak_pecah)
        for c, (nama_file, keterangan) in enumerate(isi):
            sel = t.cell(r, c)
            p = sel.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(1)
            p.add_run().add_picture(str(GAMBAR / nama_file), width=Cm(lebar_cm))
            _nomor_gambar[0] += 1
            k = sel.add_paragraph()
            k.alignment = WD_ALIGN_PARAGRAPH.CENTER
            k.paragraph_format.space_after = Pt(6)
            tambah_teks(k, f"Gambar {_nomor_gambar[0]}. ", 9, tebal=True)
            tambah_teks(k, keterangan, 9, miring=True)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def nomor_halaman(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for jenis, teks in (("begin", None), (None, "PAGE"), ("end", None)):
        run = p.add_run()
        atur_font(run, 10)
        if jenis:
            e = OxmlElement("w:fldChar")
            e.set(qn("w:fldCharType"), jenis)
        else:
            e = OxmlElement("w:instrText")
            e.set(qn("xml:space"), "preserve")
            e.text = teks
        run._element.append(e)


def ganti_halaman(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


# ---------------------------------------------------------------------------
# Isi laporan
# ---------------------------------------------------------------------------
def sampul(doc):
    """Sampul format umum laporan UMM: judul, logo, penyusun, dosen, institusi, tahun."""
    tengah = WD_ALIGN_PARAGRAPH.CENTER
    paragraf(doc, "LAPORAN TUGAS", 14, tebal=True, rata=tengah, sesudah=0)
    paragraf(doc, "PEMROGRAMAN FUNGSIONAL", 14, tebal=True, rata=tengah, sesudah=24)
    paragraf(doc, "Membangun Library Fungsional Sendiri:", 13, tebal=True, rata=tengah, sesudah=0)
    paragraf(doc, "fplib.py untuk Lima Aplikasi", 13, tebal=True, rata=tengah, sesudah=42)

    logo = GAMBAR / "00_logo_umm.png"
    if logo.exists():
        p = paragraf(doc, "", rata=tengah, sesudah=42)
        p.add_run().add_picture(str(logo), width=Cm(5.0))

    paragraf(doc, "Disusun oleh:", 12, rata=tengah, sesudah=4)
    for nama, nim, _ in IDENTITAS["anggota"]:
        paragraf(doc, f"{nama} ({nim})", 12, rata=tengah, sesudah=0)

    paragraf(doc, "Dosen Pengampu:", 12, rata=tengah, sebelum=18, sesudah=0)
    paragraf(doc, IDENTITAS["dosen"], 12, tebal=True, rata=tengah, sesudah=96)

    for teks in ("PROGRAM STUDI INFORMATIKA", "FAKULTAS TEKNIK",
                 "UNIVERSITAS MUHAMMADIYAH MALANG", "2026"):
        paragraf(doc, teks, 14, tebal=True, rata=tengah, sesudah=0)


def bab_pendahuluan(doc):
    judul(doc, "1. Pendahuluan")
    judul(doc, "1.1 Latar Belakang", 2)
    paragraf(doc, "Library adalah kumpulan fungsi siap pakai yang ditulis sekali lalu dipanggil dari program "
                  "lain melalui pernyataan `import`. Python memiliki library bawaan (`math`, `functools`, `itertools`), dapat memakai library "
                  "pihak ketiga (`numpy`, `pandas`, `requests`), dan juga memungkinkan pemrogram membuat library "
                  "sendiri berupa berkas `.py` yang diimpor dari berkas lain [8]. Ketiganya dipakai dengan cara "
                  "yang sama: diimpor, lalu fungsinya dipanggil.")
    paragraf(doc, "Tugas ini meminta kelompok membuat satu library sendiri, `fplib.py`, yang berisi fungsi-fungsi "
                  "umum bergaya fungsional, lalu memakainya di lima aplikasi: Kasir Kantin, "
                  "Presensi Kelas, Perpustakaan Mini, Keuangan Pribadi, dan Nilai Mahasiswa. Setiap fungsi "
                  "wajib dipakai oleh minimal tiga dari lima aplikasi.")
    judul(doc, "1.2 Tujuan", 2)
    for t in ("Menerapkan prinsip pemrograman fungsional (fungsi murni, fungsi tingkat tinggi, closure, "
              "komposisi) dalam sebuah library yang dapat dipakai ulang.",
              "Membuktikan bahwa satu fungsi yang sama dapat melayani kebutuhan berbeda di beberapa aplikasi "
              "hanya dengan mengganti fungsi yang dikirim sebagai argumen.",
              "Menguji library dan aplikasi secara otomatis dengan pytest [7].",
              "Menerapkan kebiasaan baik dalam memakai library: lingkungan terpisah, pencatatan versi, dan impor eksplisit."):
        poin(doc, t)
    judul(doc, "1.3 Konsep Fungsional yang Diterapkan", 2)
    tabel(doc, ["Konsep", "Penerapan di fplib"], [
        ("Fungsi murni", "Tidak ada fungsi yang mengubah data masukan. Hasil selalu dibuat baru, misalnya "
                         "dengan `sorted` dan dict baru, bukan dengan `.sort()` atau `.append()`."),
        ("Fungsi tingkat tinggi", "Fungsi menerima fungsi lain (misalnya lambda) dan mengembalikan fungsi baru [1]."),
        ("Closure", "Fungsi `hitung` di dalam `rata_rata` tetap mengingat fungsi `f` yang dibuat dari aturan, "
                    "walaupun `rata_rata` sudah selesai dijalankan."),
        ("Komposisi", "`pipe(f, g, h)` merangkai beberapa fungsi menjadi satu alur pemrosesan."),
        ("Map, filter, reduce", "`map` dipakai di `ambil`, `jumlahkan`, `rata_rata`, dan `validasi`; `filter` di `saring`, "
                                "`cari`, dan `validasi`; `reduce` di `pipe` dan `kelompokkan` [2]."),
    ], [4.0, 12.0], ukuran=10)
    paragraf(doc, "Seluruh fungsi kecuali `rupiah` dipakai dengan pola `fungsi(aturan)(data)`. Pemanggilan pertama "
                  "menerima aturan dan menghasilkan fungsi baru yang menunggu data. Karena itu, fungsi-fungsi "
                  "tersebut dapat dirangkai dengan `pipe`.")


def bab_struktur(doc):
    judul(doc, "2. Struktur Repositori dan Cara Menjalankan")
    p = paragraf(doc, f"Seluruh kode program tersimpan di repositori GitHub {IDENTITAS['repo']}.",
                 rata=WD_ALIGN_PARAGRAPH.LEFT)
    p.paragraph_format.first_line_indent = Cm(1.0)
    p.paragraph_format.line_spacing = SPASI
    paragraf(doc, "Repositori antara lain berisi `fplib.py`, `test_fplib.py`, lima berkas aplikasi, README (daftar fungsi "
                  "dan cara pakai), `MATRIKS.md` beserta pemindainya `tools/matriks.py`, dan `requirements.txt`. "
                  "Perintah untuk menjalankannya dirangkum pada tabel berikut [6].", sesudah=4)
    tabel(doc, ["Perintah", "Kegunaan"], [
        ("`python -m venv venv`", "Membuat lingkungan virtual khusus proyek."),
        ("`venv\\Scripts\\activate`", "Mengaktifkan lingkungan di Windows (Linux/macOS: `source venv/bin/activate`)."),
        ("`pip install -r requirements.txt`", "Memasang library sesuai versi yang dicatat."),
        ("`python kasir_kantin.py`", "Menjalankan aplikasi dengan data contoh (berlaku untuk kelima aplikasi)."),
        ("`python kasir_kantin.py --interaktif`", "Menjalankan aplikasi dengan data yang diketik pengguna."),
        ("`pytest -v`", "Menjalankan seluruh pengujian."),
        ("`python tools/matriks.py --cek`", "Memeriksa aturan minimal tiga aplikasi per fungsi."),
    ], [6.2, 7.8], ukuran=10)


def bab_fungsi(doc, sumber, data_matriks):
    daftar, hasil = data_matriks
    judul(doc, "3. Penjelasan Tiap Fungsi Library")
    paragraf(doc, "Parameter `kunci` dan `nilai` boleh berupa nama kolom, misalnya `\"nilai\"`, atau sebuah "
                  "fungsi. Nama kolom diubah menjadi fungsi oleh fungsi pembantu internal `_ke_fungsi` "
                  f"(fplib.py baris {sumber['_ke_fungsi'][0]}–{sumber['_ke_fungsi'][1]}). Setiap gambar kode "
                  "di bawah diambil dari editor Google Colab dengan docstring dilipat, sehingga yang tampak "
                  "hanya baris inti beserta nomor baris aslinya. Isi docstring, termasuk contoh pemakaiannya, "
                  "dapat dibaca di repositori. Aplikasi yang memakai setiap fungsi tercantum pada matriks di bab 5 "
                  "dan nomor baris pemanggilannya di bab 6.")
    for i, f in enumerate(daftar, start=1):
        awal, akhir, _ = sumber[f]
        kegunaan, cara = PENJELASAN[f]
        judul(doc, f"3.{i} {f} (fplib.py baris {awal}–{akhir})", 2)
        p = paragraf(doc, sesudah=3)
        tambah_teks(p, "Kegunaan: ", tebal=True)
        tambah_teks(p, kegunaan)
        p = paragraf(doc, sesudah=3)
        tambah_teks(p, "Cara kerja: ", tebal=True)
        tambah_teks(p, cara)
        gambar(doc, f"kode_{f}.png", f"Kode `{f}` di editor Google Colab (docstring dilipat)",
               lebar_gambar(f"kode_{f}.png", CM_PER_PX_KODE), kecil=True)


def bab_aplikasi(doc, data_matriks):
    daftar, hasil = data_matriks
    judul(doc, "4. Lima Aplikasi")
    paragraf(doc, "Setiap aplikasi memiliki dua mode. Tanpa argumen, aplikasi memakai data contoh (dipakai saat "
                  "demo); dengan `--interaktif`, aplikasi menerima data yang diketik pengguna. Kedua mode memakai "
                  "fungsi logika yang sama karena `main` menerima data sebagai argumen. Gambar di setiap subbab "
                  "adalah potongan keluaran asli dari notebook Google Colab yang mengambil (clone) repositori "
                  "GitHub; keluaran lengkap ditampilkan saat demo.")
    for i, (label, (nama, berkas, uraian)) in enumerate(APLIKASI_INFO.items(), start=1):
        dipakai = [f for f in daftar if label in hasil[f]]
        judul(doc, f"4.{i} {nama} ({berkas})", 2)
        paragraf(doc, uraian + f" Aplikasi ini memakai {len(dipakai)} fungsi fplib.", sesudah=3)
        berkas_gambar = GAMBAR_APLIKASI[label]
        gambar(doc, berkas_gambar, f"Potongan keluaran `{berkas}` di Google Colab: {KETERANGAN_KELUARAN[label]}",
               lebar_gambar(berkas_gambar, CM_PER_PX_KELUARAN), kecil=True)



def bab_bukti_jalan(doc):
    judul(doc, "4.6 Hasil Menjalankan di Google Colab", 2)
    paragraf(doc, "Gambar berikut adalah tangkapan layar asli dari notebook Google Colab yang mengambil "
                  "(clone) repositori GitHub, lalu menjalankan setiap aplikasi.", sesudah=4)
    gambar_grid(doc, [
        (GAMBAR_APLIKASI["Kasir"], "Keluaran `kasir_kantin.py`"),
        (GAMBAR_APLIKASI["Presensi"], "Keluaran `presensi_kelas.py`"),
        (GAMBAR_APLIKASI["Perpus"], "Keluaran `perpustakaan_mini.py`"),
        (GAMBAR_APLIKASI["Keuangan"], "Keluaran `keuangan_pribadi.py`"),
        (GAMBAR_APLIKASI["Nilai"], "Keluaran `nilai_mahasiswa.py`"),
        ("10_mode_interaktif.png", "Mode `--interaktif`: kode X99 ditolak `validasi`"),
    ])


def bab_matriks(doc, data_matriks):
    daftar, hasil = data_matriks
    label = [a[0] for a in matriks.APLIKASI]
    judul(doc, "5. Matriks Fungsi × Aplikasi")
    paragraf(doc, "Matriks berikut dibuat otomatis oleh `tools/matriks.py`. Program ini membaca kode kelima "
                  "aplikasi dengan modul `ast` tanpa menjalankannya [5], lalu mencatat setiap pemakaian fungsi fplib.").paragraph_format.keep_with_next = True
    tabel(doc, ["Fungsi"] + label + ["Jumlah"],
          [[f"`{f}`"] + ["✓" if l in hasil[f] else "" for l in label] + [len(hasil[f])] for f in daftar],
          [3.4, 1.9, 2.1, 1.9, 2.3, 1.9, 2.0], ukuran=10, rata_tengah=(1, 2, 3, 4, 5, 6), utuh=True)
    jumlah = [sum(1 for f in daftar if l in hasil[f]) for l in label]
    paragraf(doc, "Setiap baris memiliki minimal tiga centang dan isinya sama dengan matriks pada slide. "
                  "Jumlah fungsi yang dipakai per aplikasi: "
                  + ", ".join(f"{l} {j}" for l, j in zip(label, jumlah))
                  + f" (total {sum(jumlah)} pemakaian).")


def bab_bukti(doc, data_matriks):
    daftar, hasil = data_matriks
    judul(doc, "6. Bukti: Berkas dan Baris Pemanggilan")
    paragraf(doc, "Tabel berikut mencantumkan setiap fungsi, berkas yang memanggilnya, dan nomor baris "
                  "pemanggilannya. Di `MATRIKS.md` pada repositori GitHub, nomor baris ini berupa tautan yang "
                  "langsung membuka baris kode tersebut.")
    isi = [
        (f"`{f}`", "; ".join(
            f"`{hasil[f][l]['file']}` baris {', '.join(map(str, hasil[f][l]['baris']))}"
            for l, _ in matriks.APLIKASI if l in hasil[f]
        ))
        for f in daftar
    ]
    tabel(doc, ["Fungsi", "Berkas pemanggil dan nomor baris"], isi, [2.4, 11.6], ukuran=9)


def bab_pengujian(doc):
    ringkas, lulus, gagal = hasil_pytest()
    judul(doc, "7. Pengujian")
    paragraf(doc, f"Pengujian dijalankan dengan `pytest -v` [7]. Saat laporan ini dibuat, {lulus} pengujian "
                  f"lulus dan {gagal} gagal.")
    tabel(doc, ["Kelompok pengujian", "Yang diperiksa"], [
        ("Per fungsi library", "Kasus normal dan kasus tepi tiap fungsi (data kosong, data tidak ditemukan, "
                               "kolom hilang, nilai negatif, pembulatan rupiah) serta contoh di docstring (doctest)."),
        ("Contoh dari slide", "Tiga pemakaian `jumlahkan` (total belanja, total pengeluaran, nilai akhir berbobot)."),
        ("Sifat fungsional", "Data asli tidak berubah setelah diproses, dan hasilnya tetap sama jika dipanggil berulang."),
        ("Aturan tugas", "Setiap fungsi dipakai oleh minimal tiga aplikasi dan sesuai dengan matriks di slide; "
                         "tidak ada impor bintang (impor semua nama sekaligus)."),
        ("Aplikasi", "Kelima aplikasi berjalan tanpa galat dan angka utamanya benar."),
        ("Mode interaktif", "Masukan pengguna disimulasikan; masukan salah ditolak `validasi`, dan masukan yang terhenti (EOF) "
                            "tidak membuat program berhenti mendadak."),
    ], [4.5, 11.5], ukuran=10)
    gambar(doc, "09_pytest_hasil_matriks.png",
           f"Keluaran akhir `pytest` ({lulus} passed) dan `tools/matriks.py --cek` di Google Colab",
           lebar_gambar("09_pytest_hasil_matriks.png", CM_PER_PX_KELUARAN))


def bab_penutup(doc):
    judul(doc, "8. Penerapan Kebiasaan Baik")
    for t in ("Proyek memakai lingkungan terpisah (`python -m venv venv`) [6], dan versi library dicatat dengan "
              "`pip freeze > requirements.txt` agar semua anggota memakai versi yang sama.",
              "Impor ditulis di bagian atas berkas dan hanya untuk nama yang dibutuhkan, misalnya "
              "`from fplib import pipe, saring`. Impor bintang tidak dipakai, dan hal ini diperiksa otomatis.",
              "Fungsi yang sudah tersedia (`map`, `filter`, `sorted`, `sum`, `functools.reduce`) dipakai "
              "alih-alih menulis ulang perulangan sendiri [3].",
              "Setiap fungsi memiliki docstring sehingga penjelasannya dapat dibaca dengan `help(fplib.jumlahkan)`."):
        poin(doc, t)
    judul(doc, "9. Kesimpulan")
    paragraf(doc, "Kelompok telah membangun library `fplib.py` yang berisi sepuluh fungsi bergaya fungsional "
                  "dan dipakai oleh lima aplikasi; setiap fungsi dipakai oleh minimal tiga aplikasi sesuai "
                  "matriks. Pola `fungsi(aturan)(data)` membuat satu fungsi dapat melayani kebutuhan berbeda: "
                  "`jumlahkan` yang sama menghitung total belanja, total pengeluaran, dan nilai akhir berbobot. "
                  "Seluruh fungsi bersifat murni, terdokumentasi, dan teruji otomatis dengan pytest. Bukti pemakaian "
                  "berupa berkas dan nomor baris dihasilkan langsung dari kode oleh `tools/matriks.py` sehingga sesuai "
                  "dengan isi repositori saat laporan ini dibuat.")
    judul(doc, "Daftar Pustaka")
    for i, t in enumerate(PUSTAKA, start=1):
        p = paragraf(doc, f"[{i}] {t}", 10, rata=WD_ALIGN_PARAGRAPH.LEFT, sesudah=1)
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.first_line_indent = Cm(-0.8)
        p.paragraph_format.line_spacing = 1.0


def main():
    sumber = sumber_fungsi()
    daftar, hasil, masalah = matriks.bangun_matriks()
    salah = matriks.periksa(daftar, hasil, masalah)
    if salah:
        print("Matriks belum memenuhi aturan, laporan tidak dibuat:\n  " + "\n  ".join(salah))
        return 1
    data_matriks = (daftar, hasil)

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)  # A4
    sec.left_margin = Cm(4.0)
    sec.top_margin = sec.right_margin = sec.bottom_margin = Cm(3.0)
    gaya = doc.styles["Normal"]
    gaya.font.name = FONT
    gaya.font.size = Pt(12)
    gaya.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)

    doc.core_properties.title = "Laporan Tugas Pemrograman Fungsional — fplib.py"
    doc.core_properties.author = " & ".join(n for n, _, _ in IDENTITAS["anggota"])
    doc.core_properties.subject = "Library fungsional untuk lima aplikasi"

    sampul(doc)
    isi = doc.add_section(WD_SECTION.NEW_PAGE)
    isi.footer.is_linked_to_previous = False
    nomor_halaman(isi)

    bab_pendahuluan(doc)
    bab_struktur(doc)
    bab_fungsi(doc, sumber, data_matriks)
    bab_aplikasi(doc, data_matriks)
    bab_matriks(doc, data_matriks)
    bab_bukti(doc, data_matriks)
    bab_pengujian(doc)
    bab_penutup(doc)

    tujuan = AKAR / "laporan" / "Laporan_fplib.docx"
    doc.save(tujuan)
    print(f"Laporan dibuat: {tujuan.relative_to(AKAR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
