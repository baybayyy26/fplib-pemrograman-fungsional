# STANDAR — Cara Menulis Kode

## 1. Gaya fungsional (wajib di `fplib.py`)

| Aturan | Contoh benar | Hindari |
|---|---|---|
| Fungsi murni: tidak mengubah masukan | `sorted(data, key=...)` | `data.sort()` |
| Tidak memakai variabel global yang berubah | parameter fungsi | `global total` |
| Higher-order: terima fungsi, kembalikan fungsi | `return lambda data: ...` | fungsi yang langsung `print` |
| Pakai `map` / `filter` / `sorted` / `sum` / `reduce` | `sum(map(f, data))` | `for` + variabel penampung |
| Buat struktur baru, bukan mengubah yang lama | `{**lama, k: v}` | `lama[k] = v` |

- Pola tanda tangan fungsi library: `fungsi(aturan)(data)` agar bisa dirangkai `pipe`.
  Pengecualian yang disengaja: `rupiah(angka)` langsung mengembalikan teks.
- Parameter `kunci`/`nilai` menerima nama kolom **atau** fungsi (lewat `_ke_fungsi`).
- Setiap fungsi publik **wajib** punya docstring berisi penjelasan dan contoh `>>>`
  yang benar (diuji otomatis lewat doctest).
- Fungsi publik wajib terdaftar di `__all__`.

## 2. Struktur file aplikasi

Setiap aplikasi dibagi tiga bagian dengan urutan tetap:

1. **Data**: konstanta huruf besar, disimpan sebagai `tuple` (tidak bisa diubah).
2. **Logika**: fungsi murni / rangkaian `pipe`, tanpa `print`.
3. **Tampilan**: fungsi `main()`, satu-satunya tempat `print`.

Diakhiri dengan:

```python
if __name__ == "__main__":
    main()
```

Dengan pola ini, logika bisa diuji di `test_fplib.py` tanpa menjalankan tampilan.

## 3. Penamaan

- Bahasa Indonesia, `snake_case` untuk fungsi/variabel, `HURUF_BESAR` untuk konstanta.
- Nama menjelaskan isi: `pesanan_ditolak`, `total_belanja`, bukan `x`, `data2`.
- Lambda boleh memakai nama satu huruf yang konsisten:
  `i` item keranjang, `m` menu/mahasiswa, `t` transaksi, `k` komponen, `p` pinjaman/pesanan, `b` buku, `r` rekap/permintaan.

## 4. Import

```python
from fplib import pipe, ambil, saring     # benar: eksplisit, hanya yang dipakai
from fplib import *                       # DILARANG
```

Urutan: pustaka bawaan Python → baris kosong → `fplib`.

## 5. Pengujian

- Setiap fungsi library punya pengujian kasus normal **dan** kasus tepi (data kosong, tidak ketemu, nilai salah).
- Uji bahwa data asli tidak berubah setelah diproses.
- Nama test menjelaskan perilaku: `test_rata_rata_kosong_tidak_error`.

## 6. Format

- Indentasi 4 spasi, panjang baris ≤ 110 karakter (untuk `fplib.py`, kelima aplikasi, dan test).
- Uang selalu ditampilkan dengan `rupiah()`, tidak dengan format manual.
