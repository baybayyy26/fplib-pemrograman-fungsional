"""
Aplikasi 4 — Keuangan Pribadi
Pemasukan, pengeluaran, dan kategori.

Fungsi fplib yang dipakai: pipe, ambil, saring, urutkan, kelompokkan,
jumlahkan, rata_rata, validasi, rupiah.

Jalankan:  python keuangan_pribadi.py
"""

from fplib import pipe, ambil, saring, urutkan, kelompokkan, jumlahkan, rata_rata, validasi, rupiah

# ---------------------------------------------------------------------------
# Data (format tanggal ISO "YYYY-MM-DD" agar bisa diurutkan sebagai teks)
# ---------------------------------------------------------------------------
TRANSAKSI = (
    {"tanggal": "2026-11-01", "jenis": "masuk", "kategori": "Uang saku", "nominal": 1500000},
    {"tanggal": "2026-11-02", "jenis": "keluar", "kategori": "Makan", "nominal": 25000},
    {"tanggal": "2026-11-02", "jenis": "keluar", "kategori": "Transport", "nominal": 15000},
    {"tanggal": "2026-11-03", "jenis": "keluar", "kategori": "Kuliah", "nominal": 50000},
    {"tanggal": "2026-11-05", "jenis": "keluar", "kategori": "Makan", "nominal": 30000},
    {"tanggal": "2026-11-07", "jenis": "masuk", "kategori": "Freelance", "nominal": 400000},
    {"tanggal": "2026-11-08", "jenis": "keluar", "kategori": "Internet", "nominal": 100000},
    {"tanggal": "2026-11-10", "jenis": "keluar", "kategori": "Makan", "nominal": 27000},
    {"tanggal": "2026-11-12", "jenis": "keluar", "kategori": "Transport", "nominal": 20000},
    {"tanggal": "2026-11-14", "jenis": "keluar", "kategori": "Hiburan", "nominal": 45000},
    {"tanggal": "2026-11-15", "jenis": "keluar", "kategori": "Makan", "nominal": -5000},  # salah: negatif
    {"tanggal": "2026-11-16", "jenis": "kluar", "kategori": "Makan", "nominal": 20000},  # salah: jenis typo
)

JENIS_SAH = ("masuk", "keluar")


# ---------------------------------------------------------------------------
# Logika
# ---------------------------------------------------------------------------
cek_transaksi = validasi(
    (lambda t: t["jenis"] in JENIS_SAH, "jenis harus 'masuk' atau 'keluar'"),
    (lambda t: t["nominal"] > 0, "nominal harus lebih dari 0"),
    (lambda t: t["kategori"].strip() != "", "kategori kosong"),
)

transaksi_valid = saring(lambda t: not cek_transaksi(t))
transaksi_salah = saring(lambda t: bool(cek_transaksi(t)))
hanya_masuk = saring(lambda t: t["jenis"] == "masuk")
hanya_keluar = saring(lambda t: t["jenis"] == "keluar")


def ringkas_kategori(pasangan):
    kategori, daftar = pasangan
    return {"kategori": kategori, "total": jumlahkan("nominal")(daftar), "kali": len(daftar)}


# Alur: kelompokkan per kategori -> hitung total tiap kategori -> urutkan terbesar
pengeluaran_per_kategori = pipe(
    kelompokkan("kategori"),
    lambda kelompok: list(kelompok.items()),
    ambil(ringkas_kategori),
    urutkan("total", menurun=True),
)


def ringkasan(transaksi):
    """Hitung semua angka penting dari daftar transaksi (sudah valid)."""
    pemasukan = hanya_masuk(transaksi)
    pengeluaran = hanya_keluar(transaksi)
    masuk = jumlahkan("nominal")(pemasukan)
    keluar = jumlahkan(lambda t: t["nominal"])(pengeluaran)  # contoh persis dari slide
    return {
        "masuk": masuk,
        "keluar": keluar,
        "saldo": masuk - keluar,
        "rata_keluar": rata_rata("nominal")(pengeluaran),
        "per_kategori": pengeluaran_per_kategori(pengeluaran),
    }


# ---------------------------------------------------------------------------
# Tampilan
# ---------------------------------------------------------------------------
def main():
    print("=" * 58)
    print(" KEUANGAN PRIBADI — NOVEMBER 2026".center(58))
    print("=" * 58)

    salah = transaksi_salah(TRANSAKSI)
    if salah:
        print("\nTRANSAKSI DIABAIKAN (tidak valid)")
        print("\n".join(ambil(
            lambda t: (
                f"  {t['tanggal']} {t['jenis']:<7}{t['kategori']:<7}{rupiah(t['nominal']):>10}: "
                f"{', '.join(cek_transaksi(t))}"
            )
        )(salah)))

    valid = transaksi_valid(TRANSAKSI)
    print("\nRIWAYAT TRANSAKSI (terbaru dulu)")
    print("\n".join(ambil(
        lambda t: (
            f"  {t['tanggal']}  {'+' if t['jenis'] == 'masuk' else '-'} "
            f"{rupiah(t['nominal']):>12}  {t['kategori']}"
        )
    )(urutkan("tanggal", menurun=True)(valid))))

    r = ringkasan(valid)
    print("\nPENGELUARAN PER KATEGORI")
    print("\n".join(ambil(
        lambda k: (
            f"  {k['kategori']:<11}{rupiah(k['total']):>11}  "
            f"{k['total'] / r['keluar'] * 100 if r['keluar'] else 0:5.1f}%  ({k['kali']}x)"
        )
    )(r["per_kategori"])))

    print("-" * 58)
    print(f"  {'Total pemasukan':<32}{rupiah(r['masuk']):>14}")
    print(f"  {'Total pengeluaran':<32}{rupiah(r['keluar']):>14}")
    print(f"  {'Saldo akhir':<32}{rupiah(r['saldo']):>14}")
    print(f"  {'Rata-rata per pengeluaran':<32}{rupiah(r['rata_keluar']):>14}")
    print("=" * 58)


if __name__ == "__main__":
    main()
