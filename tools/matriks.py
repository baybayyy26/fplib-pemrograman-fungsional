"""
Pemindai matriks fungsi x aplikasi.

Membaca kode kelima aplikasi (tanpa menjalankannya) memakai modul ``ast``,
lalu mencatat di FILE dan BARIS mana setiap fungsi fplib dipanggil.
Hasilnya dipakai untuk:
- MATRIKS.md (bukti di repositori, nomor baris bisa diklik di GitHub)
- laporan (bagian "Bukti: file dan baris pemanggilan")
- pengecekan otomatis di test_fplib.py

Pemakaian (dari folder utama repo):
    python tools/matriks.py            # cetak matriks ke layar
    python tools/matriks.py --tulis    # tulis/perbarui MATRIKS.md
    python tools/matriks.py --cek      # gagal (exit 1) jika aturan dilanggar
    python tools/matriks.py --json     # keluaran JSON (dipakai pembuat laporan)
"""

import ast
import json
import sys
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent

APLIKASI = (
    ("Kasir", "kasir_kantin.py"),
    ("Presensi", "presensi_kelas.py"),
    ("Perpus", "perpustakaan_mini.py"),
    ("Keuangan", "keuangan_pribadi.py"),
    ("Nilai", "nilai_mahasiswa.py"),
)

MINIMAL_APLIKASI = 3

# Matriks persis seperti slide "Bukti wajib: matriks fungsi x aplikasi".
MATRIKS_SLIDE = {
    "pipe": {"Kasir", "Presensi", "Perpus", "Keuangan", "Nilai"},
    "ambil": {"Kasir", "Presensi", "Perpus", "Keuangan", "Nilai"},
    "saring": {"Kasir", "Presensi", "Perpus", "Keuangan", "Nilai"},
    "cari": {"Kasir", "Perpus", "Nilai"},
    "urutkan": {"Kasir", "Perpus", "Keuangan", "Nilai"},
    "kelompokkan": {"Presensi", "Perpus", "Keuangan"},
    "jumlahkan": {"Kasir", "Keuangan", "Nilai"},
    "rata_rata": {"Presensi", "Keuangan", "Nilai"},
    "validasi": {"Kasir", "Perpus", "Keuangan", "Nilai"},
    "rupiah": {"Kasir", "Perpus", "Keuangan"},
}


def fungsi_library():
    """Ambil daftar fungsi publik dari __all__ di fplib.py (tanpa import)."""
    pohon = ast.parse((AKAR / "fplib.py").read_text(encoding="utf-8"))
    for simpul in pohon.body:
        if isinstance(simpul, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "__all__" for t in simpul.targets
        ):
            return [e.value for e in simpul.value.elts]
    raise RuntimeError("__all__ tidak ditemukan di fplib.py")


def pindai_file(berkas, daftar_fungsi):
    """Kembalikan {fungsi: [nomor baris, ...]} dan daftar masalah import."""
    pohon = ast.parse((AKAR / berkas).read_text(encoding="utf-8"))
    masalah = []
    diimpor = set()
    for simpul in ast.walk(pohon):
        if isinstance(simpul, ast.ImportFrom) and simpul.module == "fplib":
            for a in simpul.names:
                if a.name == "*":
                    masalah.append(f"{berkas}:{simpul.lineno} memakai 'from fplib import *'")
                diimpor.add(a.asname or a.name)
    baris = {}
    for simpul in ast.walk(pohon):
        if (
            isinstance(simpul, ast.Name)
            and isinstance(simpul.ctx, ast.Load)
            and simpul.id in daftar_fungsi
            and simpul.id in diimpor
        ):
            baris.setdefault(simpul.id, set()).add(simpul.lineno)
    tak_terpakai = diimpor - set(baris) - {"*"}
    for nama in sorted(tak_terpakai):
        masalah.append(f"{berkas}: '{nama}' diimpor tetapi tidak dipakai")
    return {k: sorted(v) for k, v in baris.items()}, masalah


def bangun_matriks():
    daftar = fungsi_library()
    hasil = {f: {} for f in daftar}
    masalah = []
    for label, berkas in APLIKASI:
        baris, m = pindai_file(berkas, daftar)
        masalah += m
        for f, b in baris.items():
            hasil[f][label] = {"file": berkas, "baris": b}
    return daftar, hasil, masalah


def periksa(daftar, hasil, masalah):
    """Kembalikan daftar pelanggaran aturan tugas."""
    salah = list(masalah)
    for f in daftar:
        jumlah = len(hasil[f])
        if jumlah < MINIMAL_APLIKASI:
            salah.append(f"'{f}' hanya dipakai {jumlah} aplikasi (minimal {MINIMAL_APLIKASI})")
        if f in MATRIKS_SLIDE and set(hasil[f]) != MATRIKS_SLIDE[f]:
            salah.append(
                f"'{f}' dipakai di {sorted(hasil[f])}, slide meminta {sorted(MATRIKS_SLIDE[f])}"
            )
    for f in MATRIKS_SLIDE:
        if f not in daftar:
            salah.append(f"'{f}' ada di slide tetapi tidak ada di fplib.__all__")
    return salah


def ke_markdown(daftar, hasil):
    label = [a[0] for a in APLIKASI]
    out = [
        "# Matriks fungsi × aplikasi",
        "",
        "> File ini dibuat otomatis oleh `python tools/matriks.py --tulis`.",
        "> Jangan diedit manual — jalankan ulang perintah itu setelah kode berubah.",
        "",
        "| Fungsi | " + " | ".join(label) + " | Jumlah |",
        "|---|" + ":---:|" * len(label) + ":---:|",
    ]
    for f in daftar:
        sel = ["✓" if l in hasil[f] else "" for l in label]
        out.append(f"| `{f}` | " + " | ".join(sel) + f" | **{len(hasil[f])}** |")
    out += [
        "",
        f"Setiap baris minimal {MINIMAL_APLIKASI} centang. Rincian file dan baris pemanggilan di bawah",
        "(klik nomor baris untuk langsung melompat ke kodenya di GitHub).",
        "",
        "## Bukti: file dan baris pemanggilan",
        "",
    ]
    for f in daftar:
        out.append(f"### `{f}`")
        out.append("")
        out.append("| Aplikasi | File | Baris |")
        out.append("|---|---|---|")
        for l, berkas in APLIKASI:
            if l in hasil[f]:
                tautan = ", ".join(f"[{b}]({berkas}#L{b})" for b in hasil[f][l]["baris"])
                out.append(f"| {l} | [`{berkas}`]({berkas}) | {tautan} |")
        out.append("")
    return "\n".join(out)


def ke_teks(daftar, hasil):
    label = [a[0] for a in APLIKASI]
    lebar = max(map(len, daftar)) + 2
    baris = ["Fungsi".ljust(lebar) + "".join(l.center(10) for l in label) + "Jumlah"]
    for f in daftar:
        baris.append(
            f.ljust(lebar)
            + "".join(("✓" if l in hasil[f] else "·").center(10) for l in label)
            + str(len(hasil[f])).center(6)
        )
    return "\n".join(baris)


def main(argumen):
    daftar, hasil, masalah = bangun_matriks()
    if "--json" in argumen:
        print(json.dumps({"fungsi": daftar, "aplikasi": APLIKASI, "matriks": hasil}, indent=2))
        return 0
    if "--tulis" in argumen:
        (AKAR / "MATRIKS.md").write_text(ke_markdown(daftar, hasil) + "\n", encoding="utf-8")
        print("MATRIKS.md diperbarui.")
    print(ke_teks(daftar, hasil))
    salah = periksa(daftar, hasil, masalah)
    if salah:
        print("\nMASALAH:")
        print("\n".join(f"  - {s}" for s in salah))
        return 1 if "--cek" in argumen else 0
    print("\nSemua fungsi dipakai minimal 3 aplikasi dan sama dengan matriks di slide. ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
