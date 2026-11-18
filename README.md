# fplib — Library Fungsional Sendiri

Tugas **Pemrograman Fungsional · Informatika UMM**: membangun satu library
(`fplib.py`) berisi kumpulan fungsi umum bergaya fungsional, lalu memakainya
di **lima aplikasi**. Setiap fungsi dipakai oleh **minimal 3 dari 5 aplikasi**.

**Kelas:** Pemrograman Fungsional G · **Dosen:** Irtafa Masyuri, S.S.T., M.Tr.T.

**Anggota kelompok**

| No | Nama | NIM | Bagian |
|---|---|---|---|
| 1 | Aditiya Al Bayhaqy | 202410370110502 | `fplib.py`, `test_fplib.py`, Kasir Kantin, Presensi Kelas, README & repositori |
| 2 | Sigit Novriyanto | 202410370110500 | Perpustakaan Mini, Keuangan Pribadi, Nilai Mahasiswa, laporan |

---

## Struktur repositori

```
.
├── fplib.py               # LIBRARY: 10 fungsi fungsional
├── test_fplib.py          # pengujian pytest (library + 5 aplikasi + aturan matriks)
├── kasir_kantin.py        # Aplikasi 1 — menu, keranjang, total belanja
├── presensi_kelas.py      # Aplikasi 2 — kehadiran dan rekap per mahasiswa
├── perpustakaan_mini.py   # Aplikasi 3 — katalog, peminjaman, denda
├── keuangan_pribadi.py    # Aplikasi 4 — pemasukan, pengeluaran, kategori
├── nilai_mahasiswa.py     # Aplikasi 5 — komponen nilai, nilai akhir, peringkat
├── jalankan_semua.py      # skrip bantu demo (bukan aplikasi)
├── .vscode/settings.json  # pytest langsung bisa dijalankan dari panel Testing VS Code
├── MATRIKS.md             # matriks fungsi × aplikasi + file & baris (dibuat otomatis)
├── tools/matriks.py       # pemindai yang membuat MATRIKS.md
├── requirements.txt       # versi pustaka (hasil pip freeze)
├── laporan/               # buat_laporan.py → Laporan_fplib.docx & .pdf (8–12 halaman)
├── docs/                  # panduan belajar & naskah demo
└── TUGAS.md · ATURAN.md · STANDAR.md   # instruksi tugas & aturan kerja tim
```

## Persyaratan

- Python **3.10 atau lebih baru** (versi pytest di `requirements.txt` membutuhkan ≥ 3.10)
- `fplib.py` dan kelima aplikasi **hanya memakai pustaka bawaan Python**
  (`functools`, `datetime`). `pytest` hanya dibutuhkan untuk pengujian.

## Cara memasang

```bash
# 1. Buat lingkungan terpisah
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Pasang pustaka yang dicatat
pip install -r requirements.txt
```

## Cara menjalankan

```bash
python kasir_kantin.py
python presensi_kelas.py
python perpustakaan_mini.py
python keuangan_pribadi.py
python nilai_mahasiswa.py

# mode interaktif: data diketik sendiri lewat keyboard
python kasir_kantin.py --interaktif
python presensi_kelas.py --interaktif
python perpustakaan_mini.py --interaktif
python keuangan_pribadi.py --interaktif
python nilai_mahasiswa.py --interaktif

# atau semuanya sekaligus + pytest (untuk demo)
python jalankan_semua.py           # tambahkan --jeda untuk berhenti di tiap aplikasi
```

## Cara menguji

```bash
pytest -v                          # 62 pengujian
python tools/matriks.py --cek      # cek aturan "minimal 3 aplikasi" & kesesuaian dengan slide
```

---

## Daftar fungsi dan cara pakai

Semua fungsi bersifat **murni** (tidak mengubah data masukan). Kecuali `rupiah`,
setiap fungsi **mengembalikan fungsi baru** yang menunggu data, jadi pola
pemakaiannya selalu:

```python
fungsi(aturan)(data)
```

Parameter `kunci`/`nilai` boleh berupa **nama kolom** (`"nilai"`) atau **fungsi** (`lambda m: m["nilai"]`).

| Fungsi | Bentuk | Kegunaan | Hasil |
|---|---|---|---|
| `pipe` | `pipe(f1, f2, ...)(data)` | Merangkai fungsi dari kiri ke kanan | hasil fungsi terakhir |
| `ambil` | `ambil(kunci, ...)(data)` | Mengambil/mengubah tiap elemen (`map`) | `list` |
| `saring` | `saring(syarat)(data)` | Memilih elemen yang memenuhi syarat (`filter`) | `list` |
| `cari` | `cari(syarat, bawaan=None)(data)` | Elemen pertama yang memenuhi syarat | elemen / `bawaan` |
| `urutkan` | `urutkan(kunci, menurun=False)(data)` | Mengurutkan tanpa mengubah data asli | `list` |
| `kelompokkan` | `kelompokkan(kunci)(data)` | Mengelompokkan per nilai kunci | `dict` |
| `jumlahkan` | `jumlahkan(nilai)(data)` | Menjumlahkan nilai tiap elemen | angka |
| `rata_rata` | `rata_rata(nilai)(data)` | Rata-rata nilai tiap elemen (kosong → 0.0) | `float` |
| `validasi` | `validasi((syarat, pesan), ...)(item)` | Memeriksa satu data | `list` pesan kesalahan |
| `rupiah` | `rupiah(angka)` | Format angka ke teks Rupiah | `str` |

### Contoh

```python
from fplib import pipe, ambil, saring, cari, urutkan, kelompokkan, jumlahkan, rata_rata, validasi, rupiah

mhs = [
    {"nama": "Ani",   "kelas": "A", "nilai": 78},
    {"nama": "Budi",  "kelas": "A", "nilai": 85},
    {"nama": "Citra", "kelas": "B", "nilai": 62},
]

ambil("nama")(mhs)                                  # ['Ani', 'Budi', 'Citra']
saring(lambda m: m["nilai"] >= 70)(mhs)             # Ani dan Budi
cari(lambda m: m["kelas"] == "B")(mhs)              # {'nama': 'Citra', ...}
urutkan("nilai", menurun=True)(mhs)                 # Budi, Ani, Citra
kelompokkan("kelas")(mhs)                           # {'A': [Ani, Budi], 'B': [Citra]}
jumlahkan("nilai")(mhs)                             # 225
rata_rata("nilai")(mhs)                             # 75.0
rupiah(1500000)                                     # 'Rp1.500.000'

cek = validasi((lambda m: 0 <= m["nilai"] <= 100, "nilai harus 0-100"))
cek({"nilai": 105})                                 # ['nilai harus 0-100']

# Dirangkai dengan pipe: nama mahasiswa lulus, nilai tertinggi dulu
pipe(
    saring(lambda m: m["nilai"] >= 70),
    urutkan("nilai", menurun=True),
    ambil("nama"),
)(mhs)                                              # ['Budi', 'Ani']
```

Contoh `jumlahkan` yang sama dipakai tiga aplikasi, bedanya hanya fungsi yang dikirim:

```python
total  = jumlahkan(lambda i: i["harga"] * i["qty"])(keranjang)    # Kasir Kantin
keluar = jumlahkan(lambda t: t["nominal"])(pengeluaran)           # Keuangan Pribadi
akhir  = jumlahkan(lambda k: k["nilai"] * k["bobot"])(komponen)   # Nilai Mahasiswa
```

## Matriks fungsi × aplikasi

| Fungsi | Kasir | Presensi | Perpus | Keuangan | Nilai | Jumlah |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `pipe` | ✓ | ✓ | ✓ | ✓ | ✓ | **5** |
| `ambil` | ✓ | ✓ | ✓ | ✓ | ✓ | **5** |
| `saring` | ✓ | ✓ | ✓ | ✓ | ✓ | **5** |
| `cari` | ✓ |  | ✓ |  | ✓ | **3** |
| `urutkan` | ✓ |  | ✓ | ✓ | ✓ | **4** |
| `kelompokkan` |  | ✓ | ✓ | ✓ |  | **3** |
| `jumlahkan` | ✓ |  |  | ✓ | ✓ | **3** |
| `rata_rata` |  | ✓ |  | ✓ | ✓ | **3** |
| `validasi` | ✓ |  | ✓ | ✓ | ✓ | **4** |
| `rupiah` | ✓ |  | ✓ | ✓ |  | **3** |

File dan nomor baris setiap pemanggilan ada di **[MATRIKS.md](MATRIKS.md)**
(dibuat otomatis dari kode dengan `python tools/matriks.py --tulis`).

## Kebiasaan baik yang diterapkan

- Lingkungan terpisah per proyek (`venv`) dan versi dicatat di `requirements.txt`.
- Import eksplisit: `from fplib import pipe, saring`. Tidak ada `import *`
  (dicek otomatis oleh `tools/matriks.py`).
- Memakai fungsi bawaan yang sudah ada (`map`, `filter`, `sorted`, `sum`,
  `functools.reduce`) daripada menulis ulang perulangan sendiri.
- Tidak mengubah kode pustaka pihak ketiga.
