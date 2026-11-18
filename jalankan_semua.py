"""
Skrip bantu demo (BUKAN salah satu dari 5 aplikasi).

Menjalankan kelima aplikasi berurutan, lalu pytest, supaya demo
tidak perlu mengetik banyak perintah.

Jalankan:  python jalankan_semua.py
"""

import subprocess
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent

APLIKASI = (
    "kasir_kantin.py",
    "presensi_kelas.py",
    "perpustakaan_mini.py",
    "keuangan_pribadi.py",
    "nilai_mahasiswa.py",
)


def jalankan(perintah):
    print(f"\n$ {' '.join(perintah)}")
    return subprocess.run(perintah, cwd=FOLDER).returncode


def main():
    jeda = "--jeda" in sys.argv
    hasil = []
    for berkas in APLIKASI:
        hasil.append(jalankan([sys.executable, berkas]))
        if jeda:
            input("\n[Enter] untuk lanjut ke aplikasi berikutnya...")
    hasil.append(jalankan([sys.executable, "-m", "pytest", "-v"]))
    sys.exit(max(hasil))


if __name__ == "__main__":
    main()
