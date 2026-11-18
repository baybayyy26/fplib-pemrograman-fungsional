"""
Aplikasi 5 — Nilai Mahasiswa
Komponen nilai, nilai akhir, dan peringkat.

Fungsi fplib yang dipakai: pipe, ambil, saring, cari, urutkan,
jumlahkan, rata_rata, validasi.

Jalankan:  python nilai_mahasiswa.py
"""

from fplib import pipe, ambil, saring, cari, urutkan, jumlahkan, rata_rata, validasi

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def komponen(tugas, uts, uas):
    """Susun tiga komponen nilai beserta bobotnya (total bobot = 1)."""
    return (
        {"nama": "Tugas", "nilai": tugas, "bobot": 0.3},
        {"nama": "UTS", "nilai": uts, "bobot": 0.3},
        {"nama": "UAS", "nilai": uas, "bobot": 0.4},
    )


MAHASISWA = (
    {"nim": "202410370110001", "nama": "Ani", "komponen": komponen(85, 78, 90)},
    {"nim": "202410370110002", "nama": "Budi", "komponen": komponen(70, 65, 72)},
    {"nim": "202410370110003", "nama": "Citra", "komponen": komponen(92, 88, 95)},
    {"nim": "202410370110004", "nama": "Dimas", "komponen": komponen(60, 55, 48)},
    {"nim": "202410370110005", "nama": "Eka", "komponen": komponen(78, 82, 80)},
    {"nim": "202410370110006", "nama": "Fajar", "komponen": komponen(88, 105, 70)},  # salah: UTS > 100
)

# Contoh ambang nilai huruf (urut dari tertinggi).
# Sesuaikan dengan pedoman akademik yang berlaku jika berbeda.
TABEL_HURUF = (
    {"huruf": "A", "min": 80},
    {"huruf": "B+", "min": 75},
    {"huruf": "B", "min": 70},
    {"huruf": "C+", "min": 65},
    {"huruf": "C", "min": 60},
    {"huruf": "D", "min": 50},
    {"huruf": "E", "min": 0},
)

NILAI_LULUS = 60


# ---------------------------------------------------------------------------
# Logika
# ---------------------------------------------------------------------------
nilai_di_luar_rentang = saring(lambda k: not 0 <= k["nilai"] <= 100)

cek_mahasiswa = validasi(
    (lambda m: len(nilai_di_luar_rentang(m["komponen"])) == 0, "ada nilai di luar rentang 0-100"),
    (lambda m: abs(jumlahkan("bobot")(m["komponen"]) - 1) < 1e-9, "total bobot harus 1"),
)


def nilai_akhir(komponen_nilai):
    """Nilai akhir berbobot (contoh persis dari slide), dibulatkan 2 desimal.

    Pembulatan mencegah galat pecahan biner, misalnya 79.99999999 yang
    seharusnya 80 sehingga nilai huruf tidak salah.
    """
    akhir = jumlahkan(lambda k: k["nilai"] * k["bobot"])(komponen_nilai)
    return round(akhir, 2)


def huruf_dari(angka):
    return cari(lambda g: angka >= g["min"])(TABEL_HURUF)["huruf"]


def lengkapi_nilai(m):
    akhir = nilai_akhir(m["komponen"])
    return {**m, "akhir": akhir, "huruf": huruf_dari(akhir)}


# Alur: buang data tidak valid -> hitung nilai akhir -> urutkan peringkat
buat_peringkat = pipe(
    saring(lambda m: not cek_mahasiswa(m)),
    ambil(lengkapi_nilai),
    urutkan("akhir", menurun=True),
)


# ---------------------------------------------------------------------------
# Tampilan
# ---------------------------------------------------------------------------
def main():
    print("=" * 64)
    print(" NILAI MAHASISWA".center(64))
    print("=" * 64)

    ditolak = saring(lambda m: bool(cek_mahasiswa(m)))(MAHASISWA)
    if ditolak:
        print("\nDATA PERLU DIPERBAIKI")
        print("\n".join(ambil(
            lambda m: f"  {m['nim']} {m['nama']}: {', '.join(cek_mahasiswa(m))}"
        )(ditolak)))

    peringkat = buat_peringkat(MAHASISWA)
    if not peringkat:
        print("\nBelum ada data nilai yang valid.")
        return
    print("\nPERINGKAT (bobot Tugas 30%, UTS 30%, UAS 40%)")
    print(f"  {'#':<3}{'NIM':<17}{'Nama':<8}{'Tugas':>6}{'UTS':>5}{'UAS':>5}{'Akhir':>8}  Huruf")
    print("\n".join(ambil(
        lambda pasangan: (
            f"  {pasangan[0]:<3}{pasangan[1]['nim']:<17}{pasangan[1]['nama']:<8}"
            + "".join(ambil(
                lambda k: f"{k['nilai']:>{6 if k['nama'] == 'Tugas' else 5}}"
            )(pasangan[1]["komponen"]))
            + f"{pasangan[1]['akhir']:>8.2f}  {pasangan[1]['huruf']}"
        )
    )(enumerate(peringkat, start=1))))

    lulus = saring(lambda m: m["akhir"] >= NILAI_LULUS)(peringkat)
    print("-" * 64)
    print(f"  Rata-rata kelas      : {rata_rata('akhir')(peringkat):.2f}")
    print(f"  Lulus (>= {NILAI_LULUS})        : {len(lulus)} dari {len(peringkat)} mahasiswa")
    print(f"  Peringkat 1          : {peringkat[0]['nama']} ({peringkat[0]['akhir']:.2f})")
    print("=" * 64)


if __name__ == "__main__":
    main()
