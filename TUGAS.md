# TUGAS — Library Fungsional Sendiri

Ringkasan instruksi dari slide dosen (*Tugas_Library_Fungsional_Python2.pptx*,
Pemrograman Fungsional · Informatika UMM). File ini menjadi acuan utama:
**setiap perubahan kode harus tetap memenuhi semua poin di bawah.**

> ⚠️ Slide 3 ("Ketentuan tugas") dan sebagian slide 8–12 belum terbaca.
> Jika isinya menambah aturan (deadline, jumlah anggota, format, dsb.),
> tambahkan ke bagian **Ketentuan tambahan** di bawah.

## 1. Inti tugas

- Buat **satu library `fplib.py`**: satu file berisi kumpulan fungsi umum
  yang ditulis dengan **gaya fungsional**.
- Library dipakai oleh **5 aplikasi**:

| # | Aplikasi | Cakupan | File |
|---|---|---|---|
| 1 | Kasir Kantin | menu, keranjang, total belanja | `kasir_kantin.py` |
| 2 | Presensi Kelas | kehadiran dan rekap per mahasiswa | `presensi_kelas.py` |
| 3 | Perpustakaan Mini | katalog, peminjaman, denda | `perpustakaan_mini.py` |
| 4 | Keuangan Pribadi | pemasukan, pengeluaran, kategori | `keuangan_pribadi.py` |
| 5 | Nilai Mahasiswa | komponen nilai, nilai akhir, peringkat | `nilai_mahasiswa.py` |

- **Setiap fungsi dipakai oleh minimal 3 dari 5 aplikasi.**

## 2. Matriks wajib (slide "Bukti wajib")

| Fungsi | Kasir | Presensi | Perpus | Keuangan | Nilai | Jumlah |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `pipe` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `ambil` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `saring` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `cari` | ✓ |  | ✓ |  | ✓ | 3 |
| `urutkan` | ✓ |  | ✓ | ✓ | ✓ | 4 |
| `kelompokkan` |  | ✓ | ✓ | ✓ |  | 3 |
| `jumlahkan` | ✓ |  |  | ✓ | ✓ | 3 |
| `rata_rata` |  | ✓ |  | ✓ | ✓ | 3 |
| `validasi` | ✓ |  | ✓ | ✓ | ✓ | 4 |
| `rupiah` | ✓ |  | ✓ | ✓ |  | 3 |

*Wajib ada di laporan. Setiap baris minimal 3 centang, dilengkapi nama file pemanggilnya.*

Kesesuaian kode dengan matriks ini **dicek otomatis** oleh
`python tools/matriks.py --cek` dan oleh `pytest`.

## 3. Contoh gaya dari slide ("Satu fungsi, tiga aplikasi: jumlahkan")

```python
# di library
def jumlahkan(nilai):
    return lambda data: sum(map(nilai, data))

total  = jumlahkan(lambda i: i["harga"] * i["qty"])(keranjang)    # Kasir: total belanja
keluar = jumlahkan(lambda t: t["nominal"])(pengeluaran)           # Keuangan: total pengeluaran
akhir  = jumlahkan(lambda k: k["nilai"] * k["bobot"])(komponen)   # Nilai: nilai akhir berbobot
```

*Fungsinya sama, yang berbeda hanya cara menghitung nilai yang dikirim sebagai argumen.*

## 4. Kebiasaan baik (slide "Cara memakai library dengan baik")

- [x] Lingkungan terpisah per proyek (`python -m venv venv`)
- [x] Catat versi: `pip freeze > requirements.txt`
- [x] Import di bagian atas file, ambil yang perlu saja (`from fplib import pipe, saring`)
- [x] Hindari `import *`
- [x] Jangan mengubah kode di dalam library pihak ketiga
- [x] Pakai fungsi library yang sudah ada sebelum menulis ulang sendiri
- [x] Baca dokumentasi / `help()` sebelum memakai fungsi (semua fungsi fplib punya docstring)

## 5. Tiga luaran yang dikumpulkan

### ① Repositori (GitHub)
- [x] `fplib.py` dan `test_fplib.py`
- [x] 5 file aplikasi yang bisa dijalankan
- [x] README: daftar fungsi dan cara pakai

### ② Laporan (PDF, 8–12 halaman)
- [x] Penjelasan tiap fungsi library
- [x] Matriks fungsi × aplikasi
- [x] Bukti: file dan baris pemanggilan
- [x] Nama anggota dan NIM di sampul
- [x] Tabel pembagian tugas anggota
- [x] Tautan repositori GitHub
- [x] Kelas dan nama dosen di sampul

### ③ Demo (10 menit + 5 menit tanya jawab)
- [ ] Jalankan kelima aplikasi
- [ ] Jalankan pytest
- [ ] **Semua anggota berbicara** (lihat `docs/NASKAH_DEMO.md`)

## 6. Ketentuan tambahan (isi setelah slide 3 terbaca)

- Deadline: _[...]_
- Jumlah anggota: 2 (Aditiya Al Bayhaqy 202410370110502, Sigit Novriyanto 202410370110500)
- Kelas: Pemrograman Fungsional G
- Dosen: Irtafa Masyuri, S.S.T., M.Tr.T.
- Lainnya: _[...]_
