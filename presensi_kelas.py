"""
Aplikasi 2 — Presensi Kelas
Kehadiran dan rekap per mahasiswa.

Fungsi fplib yang dipakai: pipe, ambil, saring, kelompokkan, rata_rata.

Jalankan:  python presensi_kelas.py
"""

from fplib import pipe, ambil, saring, kelompokkan, rata_rata

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
# Kode status: H = hadir, I = izin, S = sakit, A = alpa.
# Satu huruf = satu pertemuan (pertemuan 1 s.d. 8).
RIWAYAT = (
    ("202410370110001", "Ani", "HHHHHHHH"),
    ("202410370110002", "Budi", "HHIHHHAH"),
    ("202410370110003", "Citra", "HAHAHSHA"),
    ("202410370110004", "Dimas", "HHHHSHHH"),
    ("202410370110005", "Eka", "AHAHIHAH"),
)

# Ubah riwayat ringkas menjadi satu catatan per mahasiswa per pertemuan.
PRESENSI = tuple(
    {"nim": nim, "nama": nama, "pertemuan": ke + 1, "status": status}
    for nim, nama, baris in RIWAYAT
    for ke, status in enumerate(baris)
)

BATAS_MINIMAL = 75  # persen kehadiran minimal untuk ikut ujian


# ---------------------------------------------------------------------------
# Logika
# ---------------------------------------------------------------------------
persen_hadir = rata_rata(lambda c: 100 if c["status"] == "H" else 0)
hanya_hadir = saring(lambda c: c["status"] == "H")


def rekap_satu(catatan):
    """Rekap untuk satu mahasiswa dari semua catatannya."""
    return {
        "nim": catatan[0]["nim"],
        "nama": catatan[0]["nama"],
        "hadir": len(hanya_hadir(catatan)),
        "pertemuan": len(catatan),
        "persen": persen_hadir(catatan),
    }


# Alur: kelompokkan per NIM -> ambil isi tiap kelompok -> buat rekap tiap mahasiswa
rekap_per_mahasiswa = pipe(
    kelompokkan("nim"),
    lambda kelompok: list(kelompok.values()),
    ambil(rekap_satu),
)

# Alur: kelompokkan per pertemuan -> persentase hadir tiap pertemuan
rekap_per_pertemuan = pipe(
    kelompokkan("pertemuan"),
    lambda kelompok: list(kelompok.items()),
    ambil(lambda pasangan: {"pertemuan": pasangan[0], "persen": persen_hadir(pasangan[1])}),
)

tidak_memenuhi_syarat = saring(lambda r: r["persen"] < BATAS_MINIMAL)


# ---------------------------------------------------------------------------
# Tampilan
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print(" PRESENSI KELAS".center(60))
    print("=" * 60)

    rekap = rekap_per_mahasiswa(PRESENSI)
    print("\nREKAP PER MAHASISWA")
    print(f"  {'NIM':<17}{'Nama':<8}{'Hadir':>6}{'Persen':>9}  Status")
    print("\n".join(ambil(
        lambda r: (
            f"  {r['nim']:<17}{r['nama']:<8}{str(r['hadir']) + '/' + str(r['pertemuan']):>6}"
            f"{r['persen']:>8.1f}%  "
            f"{'boleh ujian' if r['persen'] >= BATAS_MINIMAL else 'TIDAK boleh ujian'}"
        )
    )(rekap)))

    print("\nKEHADIRAN PER PERTEMUAN")
    print("\n".join(ambil(
        lambda p: f"  Pertemuan {p['pertemuan']}: {p['persen']:5.1f}%"
    )(rekap_per_pertemuan(PRESENSI))))

    kurang = tidak_memenuhi_syarat(rekap)
    print(f"\nRata-rata kehadiran kelas : {rata_rata('persen')(rekap):.1f}%")
    print(f"Di bawah {BATAS_MINIMAL}%           : {', '.join(ambil('nama')(kurang)) or '-'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
