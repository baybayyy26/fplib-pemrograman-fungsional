"""
Aplikasi 3 — Perpustakaan Mini
Katalog, peminjaman, dan denda.

Fungsi fplib yang dipakai: pipe, ambil, saring, cari, urutkan,
kelompokkan, validasi, rupiah.

Jalankan:  python perpustakaan_mini.py
"""

from datetime import date

from fplib import pipe, ambil, saring, cari, urutkan, kelompokkan, validasi, rupiah

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
KATALOG = (
    {"kode": "B01", "judul": "Belajar Python Dasar", "kategori": "Pemrograman", "tahun": 2021, "stok": 2},
    {"kode": "B02", "judul": "Struktur Data", "kategori": "Pemrograman", "tahun": 2019, "stok": 1},
    {"kode": "B03", "judul": "Jaringan Komputer", "kategori": "Jaringan", "tahun": 2020, "stok": 2},
    {"kode": "B04", "judul": "Basis Data", "kategori": "Data", "tahun": 2022, "stok": 1},
    {"kode": "B05", "judul": "Pengantar Statistika", "kategori": "Data", "tahun": 2018, "stok": 1},
    {"kode": "B06", "judul": "Keamanan Jaringan", "kategori": "Jaringan", "tahun": 2023, "stok": 1},
)

# tgl_kembali = None artinya buku belum dikembalikan.
PEMINJAMAN = (
    {"id": "P01", "kode": "B01", "peminjam": "Ani",
     "tgl_pinjam": date(2026, 11, 1), "tgl_kembali": date(2026, 11, 6)},
    {"id": "P02", "kode": "B02", "peminjam": "Budi",
     "tgl_pinjam": date(2026, 11, 2), "tgl_kembali": None},
    {"id": "P03", "kode": "B04", "peminjam": "Citra",
     "tgl_pinjam": date(2026, 11, 3), "tgl_kembali": date(2026, 11, 14)},
    {"id": "P04", "kode": "B03", "peminjam": "Dimas",
     "tgl_pinjam": date(2026, 11, 12), "tgl_kembali": None},
    {"id": "P05", "kode": "B06", "peminjam": "Eka",
     "tgl_pinjam": date(2026, 11, 5), "tgl_kembali": None},
)

# Permintaan pinjam baru (dua terakhir sengaja salah)
PERMINTAAN_BARU = (
    {"kode": "B05", "peminjam": "Fajar"},
    {"kode": "B02", "peminjam": "Gita"},  # salah: stok B02 sedang dipinjam semua
    {"kode": "B99", "peminjam": "Hana"},  # salah: kode buku tidak ada
)

# Tanggal acuan dibuat tetap agar hasil demo selalu sama.
HARI_INI = date(2026, 11, 17)
LAMA_PINJAM_HARI = 7
DENDA_PER_HARI = 1000


# ---------------------------------------------------------------------------
# Logika
# ---------------------------------------------------------------------------
def cari_buku(kode):
    return cari(lambda b: b["kode"] == kode)(KATALOG)


masih_dipinjam = saring(lambda p: p["tgl_kembali"] is None)


def sisa_stok(kode):
    """Stok buku dikurangi peminjaman yang belum kembali."""
    buku = cari_buku(kode)
    aktif = saring(lambda p: p["kode"] == kode)(masih_dipinjam(PEMINJAMAN))
    return buku["stok"] - len(aktif)


def hari_terlambat(pinjam):
    selesai = pinjam["tgl_kembali"] or HARI_INI
    return max(0, (selesai - pinjam["tgl_pinjam"]).days - LAMA_PINJAM_HARI)


def lengkapi_denda(pinjam):
    terlambat = hari_terlambat(pinjam)
    return {
        **pinjam,
        "judul": cari_buku(pinjam["kode"])["judul"],
        "terlambat": terlambat,
        "denda": terlambat * DENDA_PER_HARI,
    }


# Alur: hitung denda -> ambil yang terlambat saja -> urutkan denda terbesar
daftar_denda = pipe(
    ambil(lengkapi_denda),
    saring(lambda p: p["denda"] > 0),
    urutkan("denda", menurun=True),
)

# Alur: urutkan kategori lalu judul -> kelompokkan per kategori (urutan tetap terjaga)
katalog_per_kategori = pipe(
    urutkan(lambda b: (b["kategori"], b["judul"])),
    kelompokkan("kategori"),
)

cek_permintaan = validasi(
    (lambda r: cari_buku(r["kode"]) is not None, "kode buku tidak ditemukan"),
    (lambda r: cari_buku(r["kode"]) is None or sisa_stok(r["kode"]) > 0, "stok buku sedang habis"),
    (lambda r: r["peminjam"].strip() != "", "nama peminjam kosong"),
)


# ---------------------------------------------------------------------------
# Tampilan
# ---------------------------------------------------------------------------
def main():
    print("=" * 62)
    print(" PERPUSTAKAAN MINI".center(62))
    print(f" Tanggal acuan: {HARI_INI:%d-%m-%Y}".center(62))
    print("=" * 62)

    print("\nKATALOG PER KATEGORI")
    for kategori, buku in katalog_per_kategori(KATALOG).items():
        print(f"  [{kategori}]")
        print("\n".join(ambil(
            lambda b: (
                f"    {b['kode']}  {b['judul']:<24} {b['tahun']}  "
                f"sisa {sisa_stok(b['kode'])}/{b['stok']}"
            )
        )(buku)))

    print("\nDENDA KETERLAMBATAN (batas pinjam "
          f"{LAMA_PINJAM_HARI} hari, {rupiah(DENDA_PER_HARI)}/hari)")
    print("\n".join(ambil(
        lambda p: (
            f"  {p['id']}  {p['peminjam']:<7}{p['judul']:<22}"
            f"{p['terlambat']:>3} hari  {rupiah(p['denda']):>8}"
            f"{'  (belum kembali)' if p['tgl_kembali'] is None else ''}"
        )
    )(daftar_denda(PEMINJAMAN))))

    print("\nPERMINTAAN PINJAM BARU")
    print("\n".join(ambil(
        lambda r: f"  {r['peminjam']:<6} {r['kode']}: " + (
            "DISETUJUI" if not cek_permintaan(r)
            else "DITOLAK - " + ", ".join(cek_permintaan(r))
        )
    )(PERMINTAAN_BARU)))
    print("=" * 62)


if __name__ == "__main__":
    main()
