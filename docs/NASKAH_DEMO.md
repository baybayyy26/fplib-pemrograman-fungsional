# Naskah Demo — 10 menit + 5 menit tanya jawab

Syarat dari slide: **jalankan kelima aplikasi**, **jalankan pytest**, dan
**semua anggota berbicara**. Naskah ini untuk 2 anggota: **Bayhaqy** dan **Sigit**,
masing-masing berbicara sekitar 5 menit.

## Persiapan (H-1 dan 10 menit sebelum maju)

- [ ] Clone repo bersih dari GitHub di laptop demo, lalu buat venv dan `pip install -r requirements.txt`
- [ ] Coba sekali: `python jalankan_semua.py` → semua tampil, pytest **56 passed**
- [ ] Perbesar huruf terminal (Ctrl + `+`), tema terang/kontras tinggi
- [ ] Buka VS Code dengan tab: `fplib.py`, `MATRIKS.md`, dan aplikasi masing-masing
- [ ] Aktifkan venv, `cls`/`clear` terminal
- [ ] Siapkan stopwatch; yang tidak sedang bicara memberi kode "1 menit lagi"
- [ ] Pytest juga bisa dijalankan dari panel **Testing** (ikon tabung) di VS Code

## Susunan waktu

| Menit | Pembicara | Isi | Perintah / yang ditunjukkan |
|---|---|---|---|
| 0:00–1:30 | Bayhaqy | Pembuka + library | Tunjukkan `fplib.py` |
| 1:30–3:15 | Bayhaqy | Kasir Kantin | `python kasir_kantin.py` |
| 3:15–5:00 | Bayhaqy | Presensi Kelas | `python presensi_kelas.py` |
| 5:00–6:30 | Sigit | Perpustakaan Mini | `python perpustakaan_mini.py` |
| 6:30–8:00 | Sigit | Keuangan Pribadi | `python keuangan_pribadi.py` |
| 8:00–9:15 | Sigit | Nilai Mahasiswa | `python nilai_mahasiswa.py` |
| 9:15–10:00 | Sigit → Bayhaqy | pytest + matriks + penutup | `pytest -v`, `python tools/matriks.py --cek` |
| 10:00–15:00 | Berdua | Tanya jawab | Bayhaqy: library, Kasir, Presensi. Sigit: Perpus, Keuangan, Nilai |

## Naskah per bagian

### Bayhaqy — Pembuka & library (1:30)
> "Kami membangun satu library, `fplib.py`, berisi 10 fungsi bergaya fungsional:
> pipe, ambil, saring, cari, urutkan, kelompokkan, jumlahkan, rata_rata,
> validasi, dan rupiah. Semua fungsi murni: tidak mengubah data masukan.
> Polanya seperti contoh `jumlahkan` di slide: `fungsi(aturan)(data)`.
> Karena semua hasilnya berbentuk fungsi yang menerima data, fungsi-fungsi
> ini bisa dirangkai dengan `pipe`. Library ini dipakai lima aplikasi, dan
> setiap fungsi dipakai minimal tiga aplikasi."

Tunjukkan: `jumlahkan` (2 baris) dan `pipe` (1 baris) di `fplib.py`.

### Bayhaqy — Kasir Kantin (1:45)
Jalankan, lalu tunjukkan:
1. Menu diurutkan dengan `urutkan("harga")`.
2. **Pesanan ditolak**: qty 0 dan kode X99 ditolak oleh `validasi`.
3. Alur `buat_keranjang = pipe(saring, ambil, urutkan)`, dengan `cari` untuk mencocokkan kode menu.
4. Total memakai `jumlahkan(lambda i: i["harga"] * i["qty"])`, sama persis dengan slide → **Rp52.000**.

### Bayhaqy — Presensi Kelas (1:45)
1. `kelompokkan("nim")` mengubah 40 catatan menjadi 5 kelompok mahasiswa.
2. Persentase hadir = `rata_rata(lambda c: 100 if H else 0)`. Rata-rata dari 100/0 sama dengan persentase.
3. `saring(persen < 75)` menghasilkan **Citra, Eka** yang tidak boleh ujian.
4. Rekap per pertemuan memakai `kelompokkan("pertemuan")` yang sama.

### Sigit — Perpustakaan Mini (1:30)
1. Katalog: `urutkan((kategori, judul))` lalu `kelompokkan("kategori")` dalam satu `pipe`.
2. Denda: `pipe(ambil(lengkapi_denda), saring(denda > 0), urutkan(denda ↓))`, dengan Budi terlambat 8 hari = **Rp8.000**.
3. Permintaan pinjam: `validasi` menolak stok habis dan kode tidak ada, masing-masing dengan alasannya.

### Sigit — Keuangan Pribadi (1:30)
1. Dua transaksi salah (nominal negatif, jenis typo) diabaikan oleh `validasi`.
2. `keluar = jumlahkan(lambda t: t["nominal"])(pengeluaran)`, sama dengan slide.
3. `kelompokkan("kategori")` → total per kategori → `urutkan` terbesar (Internet).
4. Saldo **Rp1.588.000**, rata-rata pengeluaran memakai `rata_rata`.

### Sigit — Nilai Mahasiswa (1:15)
1. Fajar ditolak `validasi` karena UTS 105.
2. `akhir = jumlahkan(lambda k: k["nilai"] * k["bobot"])(komponen)`, sama dengan slide.
3. Nilai huruf dicari dengan `cari(angka >= min)` di tabel yang urut dari tertinggi.
4. Peringkat `urutkan("akhir", menurun=True)`; Citra peringkat 1 (92,00).

### Sigit — pytest, lalu Bayhaqy menutup (0:45)
```bash
pytest -v
python tools/matriks.py --cek
```
> "Ada 56 pengujian: setiap fungsi diuji untuk kasus normal dan kasus tepi,
> diuji bahwa data asli tidak berubah, dan ada test yang membaca kode kelima
> aplikasi untuk memastikan setiap fungsi dipakai minimal tiga aplikasi sesuai
> matriks. File dan baris pemanggilannya ada di MATRIKS.md dan di laporan."

Bayhaqy menutup: "Terima kasih, kami siap menerima pertanyaan."

## Rencana cadangan

| Masalah | Tindakan |
|---|---|
| `pytest` tidak ditemukan | venv belum aktif → `venv\Scripts\activate`, atau `python -m pytest -v` |
| Waktu mepet | `python jalankan_semua.py` (semua aplikasi + pytest sekali jalan) |
| Laptop bermasalah | Repo sudah di-clone di laptop anggota lain |
| Ditanya "coba ubah data" | Ubah satu angka di bagian **Data** aplikasi, jalankan ulang; logika tidak perlu disentuh |
