# ATURAN — Alur Kerja Tim

Baca **TUGAS.md** (apa yang diminta dosen) dan **STANDAR.md** (cara menulis kode)
sebelum mengubah apa pun.

## 1. Pembagian kerja

- Bayhaqy: `fplib.py`, `test_fplib.py`, Kasir Kantin, Presensi Kelas, README & repositori.
- Sigit: Perpustakaan Mini, Keuangan Pribadi, Nilai Mahasiswa, laporan.
- Perubahan `fplib.py` harus disetujui kedua anggota karena dipakai semua aplikasi.
- Tulis pembagian final di tabel anggota pada README.md dan di laporan.

## 2. Alur Git

```bash
git checkout main && git pull                 # selalu mulai dari main terbaru
git checkout -b fitur/presensi-rekap          # 1 cabang = 1 pekerjaan
# ... ubah kode ...
pytest -v && python tools/matriks.py --cek    # WAJIB lulus sebelum commit
python tools/matriks.py --tulis               # perbarui MATRIKS.md jika ada pemakaian fungsi berubah
git add <file yang diubah>
git commit -m "feat(presensi): rekap kehadiran per pertemuan"
git push -u origin fitur/presensi-rekap       # lalu buat Pull Request ke main
```

- **Jangan push langsung ke `main`.** Gabungkan lewat Pull Request yang dicek minimal satu anggota lain.
- Hapus cabang setelah digabung (`git branch -d <cabang>` dan hapus di GitHub).
- Jangan commit `venv/`, `__pycache__/`, `.pytest_cache/` (sudah ada di `.gitignore`).

## 3. Format pesan commit

```
<jenis>(<bagian>): <ringkasan singkat dalam bahasa Indonesia>
```

| Jenis | Dipakai untuk |
|---|---|
| `feat` | fitur/fungsi baru |
| `fix` | perbaikan bug |
| `test` | menambah/mengubah pengujian |
| `docs` | README, laporan, panduan |
| `refactor` | merapikan kode tanpa mengubah hasil |

Bagian: `fplib`, `kasir`, `presensi`, `perpus`, `keuangan`, `nilai`, `repo`.

## 4. Syarat sebelum Pull Request digabung

- [ ] `pytest -v` lulus semua
- [ ] `python tools/matriks.py --cek` tidak menampilkan MASALAH
- [ ] Kelima aplikasi masih jalan (`python jalankan_semua.py`)
- [ ] `MATRIKS.md` sudah diperbarui jika baris pemanggilan berubah
- [ ] Tidak ada `import *`, tidak ada fungsi fplib yang diimpor tapi tidak dipakai

## 5. Aturan yang tidak boleh dilanggar

1. Setiap fungsi di `fplib.__all__` dipakai **minimal 3 dari 5 aplikasi** dan
   **persis sesuai matriks di slide** (lihat TUGAS.md bagian 2).
2. Jangan menambah/menghapus pemakaian fungsi di aplikasi tanpa memeriksa ulang matriks.
3. Jangan mengedit `MATRIKS.md` secara manual.
4. Setelah kode berubah, **nomor baris di laporan ikut berubah**: buat ulang laporan
   (`python laporan/buat_laporan.py`) sebelum dikumpulkan.
