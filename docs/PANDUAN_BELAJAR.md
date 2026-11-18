# Panduan Belajar fplib — dari dasar sampai siap ditanya dosen

Semua rujukan file dan baris di panduan ini bisa diklik. Di GitHub, tautannya
langsung melompat ke baris yang dimaksud.

---

## Bagian 0 — Lima konsep dasar

### 0.1 Fungsi murni (*pure function*)
**Definisi:** fungsi yang hasilnya hanya ditentukan oleh argumennya dan tidak
mengubah apa pun di luar dirinya (tidak mengubah list masukan, tidak `print`,
tidak mengubah variabel global).

**Analogi:** kalkulator. Tekan `2 + 3`, hasilnya selalu `5`, dan kalkulator
tidak diam-diam mengubah angka di kertasmu.

```python
def murni(data):        return sorted(data)   # data asli tetap
def tidak_murni(data):  data.sort()           # data asli BERUBAH
```

Di repo ini, sifat ini **diuji**: `test_data_asli_tidak_berubah` di
[test_fplib.py](../test_fplib.py) menyalin data, menjalankan fungsi, lalu
memastikan data tetap sama.

### 0.2 Fungsi sebagai nilai (*first-class function*) dan `lambda`
Di Python, fungsi bisa disimpan di variabel dan dikirim sebagai argumen,
sama seperti angka atau teks. `lambda` adalah cara menulis fungsi kecil tanpa nama.

```python
kali_dua = lambda x: x * 2      # sama dengan: def kali_dua(x): return x * 2
kali_dua(4)                     # 8
```

### 0.3 Fungsi tingkat tinggi (*higher-order function*)
Fungsi yang **menerima** fungsi lain dan/atau **mengembalikan** fungsi.
Semua fungsi fplib (kecuali `rupiah`) termasuk jenis ini.

### 0.4 Closure dan pola `fungsi(aturan)(data)`
**Analogi:** mesin cetak kue. `jumlahkan(cara_hitung)` adalah tahap *memasang
cetakan* dan belum ada adonan. Hasilnya mesin yang siap dipakai. Setelah itu
`(data)` adalah *memasukkan adonan*.

```python
hitung_total = jumlahkan(lambda i: i["harga"] * i["qty"])  # pasang cetakan → dapat FUNGSI
hitung_total(keranjang)                                    # masukkan adonan → dapat ANGKA
jumlahkan(lambda i: i["harga"] * i["qty"])(keranjang)      # sama, ditulis sekaligus
```

Fungsi yang dikembalikan "mengingat" `cara_hitung` walaupun `jumlahkan`
sudah selesai berjalan. Ingatan inilah yang disebut **closure**.

**Kenapa pola ini dipilih?** Karena semua fungsi yang dihasilkan punya bentuk
sama, yaitu `f(data) -> hasil`. Bentuk yang seragam membuatnya bisa
**disambung-sambung dengan `pipe`**.

### 0.5 Komposisi (merangkai fungsi)
**Analogi:** jalur produksi pabrik. Bahan masuk ke mesin 1, hasilnya langsung
masuk ke mesin 2, lalu ke mesin 3. `pipe(mesin1, mesin2, mesin3)` membangun
jalur itu.

---

## Bagian 1 — Bedah tiap fungsi di `fplib.py`

### `_ke_fungsi(kunci)` — pembantu internal · [fplib.py#L41](../fplib.py#L41)
**Fungsinya:** menyeragamkan masukan. Kalau `kunci` sudah fungsi, kembalikan
apa adanya. Kalau berupa nama kolom (`"nilai"`), ubah menjadi
`lambda item: item["nilai"]` ([baris 51](../fplib.py#L51)).

**Kenapa ada:** supaya pengguna boleh menulis `urutkan("nilai")` (singkat) atau
`urutkan(lambda m: m["nilai"] * 2)` (fleksibel). Fungsi ini dipakai oleh `ambil`,
`urutkan`, `kelompokkan`, `jumlahkan`, dan `rata_rata`. Diawali `_` karena ini
urusan dalam library, bukan untuk aplikasi, sehingga tidak masuk `__all__` dan
tidak dihitung di matriks.

---

### 1. `pipe(*langkah)` · [fplib.py#L54](../fplib.py#L54)
**Definisi:** merangkai beberapa fungsi menjadi satu; dijalankan **kiri ke kanan**.
`pipe(f, g, h)(x)` sama dengan `h(g(f(x)))`.

**Kode inti** ([baris 67](../fplib.py#L67)):
```python
return lambda data: reduce(lambda hasil, f: f(hasil), langkah, data)
```

**Bedah per bagian:**
| Bagian | Arti |
|---|---|
| `*langkah` | menampung berapa pun fungsi menjadi tuple, mis. `(f, g, h)` |
| `lambda data:` | yang dikembalikan adalah fungsi yang menunggu data |
| `reduce(..., langkah, data)` | mulai dari `data`, lalu "lipat" satu per satu fungsi di `langkah` |
| `lambda hasil, f: f(hasil)` | aturan lipatnya: hasil sejauh ini dimasukkan ke fungsi berikutnya |

**Jejak eksekusi** `pipe(tambah1, kali2)(3)`:
```
hasil = 3            (nilai awal)
hasil = tambah1(3) = 4
hasil = kali2(4)   = 8   → dikembalikan
```

**Dipakai di:** kelima aplikasi, misalnya alur keranjang
[kasir_kantin.py#L61](../kasir_kantin.py#L61) dan rekap
[presensi_kelas.py#L54](../presensi_kelas.py#L54).

---

### 2. `ambil(*kunci)` · [fplib.py#L70](../fplib.py#L70)
**Definisi:** mengubah setiap elemen data, yaitu versi fungsional dari `map`.
Tiga mode ([baris 86–92](../fplib.py#L86)):

| Panggilan | Hasil |
|---|---|
| `ambil("nama")` | daftar nilai kolom `nama` |
| `ambil("nama", "nilai")` | daftar dict berisi kolom itu saja |
| `ambil(fungsi)` | daftar hasil fungsi tiap elemen |

**Analogi:** stempel. Setiap kertas yang lewat distempel dengan cara yang sama.

**Penerapan menarik:** di aplikasi, `ambil` juga dipakai untuk **membuat baris
teks tampilan**. Contohnya [kasir_kantin.py#L84](../kasir_kantin.py#L84): setiap
menu diubah menjadi satu baris string, lalu disatukan dengan `"\n".join(...)`.
Tidak ada `for` + `print` berulang.

---

### 3. `saring(predikat)` · [fplib.py#L95](../fplib.py#L95)
**Definisi:** memilih elemen yang membuat `predikat` bernilai `True`, yaitu
versi fungsional dari `filter`. **Predikat** = fungsi yang menjawab ya/tidak.

**Analogi:** saringan pasir. Yang lolos lubang (memenuhi syarat) jatuh ke wadah.

```python
return lambda data: list(filter(predikat, data))     # baris 101
```
`filter` menghasilkan *iterator* (malas, belum dihitung). `list(...)` memaksa
hasilnya menjadi list supaya bisa dipakai berkali-kali.

**Dipakai di:** memisahkan pesanan valid/ditolak
([kasir_kantin.py#L62](../kasir_kantin.py#L62)), pemasukan vs pengeluaran
([keuangan_pribadi.py#L45](../keuangan_pribadi.py#L45)), dan lainnya.

---

### 4. `cari(predikat, bawaan=None)` · [fplib.py#L104](../fplib.py#L104)
**Definisi:** mengembalikan elemen **pertama** yang cocok, atau `bawaan` jika tidak ada.

```python
return lambda data: next(filter(predikat, data), bawaan)    # baris 113
```
- `filter(...)` membuat iterator elemen yang cocok (belum dihitung semua).
- `next(iterator, bawaan)` mengambil **satu** elemen pertama lalu berhenti.
  Jadi pencarian langsung selesai saat ketemu, tidak memeriksa sisa data.
- Jika iterator kosong, `next` mengembalikan `bawaan`, bukan error.

**Beda dengan `saring`:** `saring` → *semua* yang cocok (list); `cari` → *satu* (elemen).

**Dipakai di:** mencari menu per kode ([kasir_kantin.py#L45](../kasir_kantin.py#L45)),
buku per kode ([perpustakaan_mini.py#L58](../perpustakaan_mini.py#L58)), dan
**nilai huruf** ([nilai_mahasiswa.py#L71](../nilai_mahasiswa.py#L71)). Tabel huruf
diurutkan dari ambang tertinggi, sehingga ambang pertama yang `angka >= min`
adalah huruf yang benar.

---

### 5. `urutkan(kunci, menurun=False)` · [fplib.py#L116](../fplib.py#L116)
**Definisi:** mengurutkan memakai `sorted`, yang **membuat list baru**. Ini
berbeda dengan `list.sort()` yang mengubah list asli, sehingga tidak murni.

**Sifat penting:** `sorted` di Python **stabil**: elemen dengan kunci sama
mempertahankan urutan awalnya (diuji di `test_urutkan_stabil_untuk_nilai_sama`).

**Kunci tuple:** [perpustakaan_mini.py#L95](../perpustakaan_mini.py#L95) memakai
`urutkan(lambda b: (b["kategori"], b["judul"]))`. Tuple dibandingkan dari elemen
pertama, jadi hasilnya urut per kategori, lalu per judul di dalamnya.

---

### 6. `kelompokkan(kunci)` · [fplib.py#L126](../fplib.py#L126)
**Definisi:** mengubah list menjadi `dict {nilai_kunci: [elemen, ...]}`.

**Kode inti** ([baris 139–143](../fplib.py#L139)):
```python
def tambahkan(kelompok, item):
    k = ambil_kunci(item)
    return {**kelompok, k: kelompok.get(k, []) + [item]}
return lambda data: reduce(tambahkan, data, {})
```
- `reduce(tambahkan, data, {})`: mulai dari dict kosong, lalu tiap elemen "ditambahkan".
- `{**kelompok, k: ...}`: **membuat dict baru** berisi isi lama ditambah/diganti kunci `k`.
- `kelompok.get(k, [])`: ambil list kelompok `k`; kalau belum ada, mulai dari `[]`.
- `+ [item]`: **membuat list baru**, bukan `.append()` yang mengubah list lama.

**Jejak** data kelas `A, B, A`:
```
{}                          → {A:[Ani]}
{A:[Ani]}                   → {A:[Ani], B:[Citra]}
{A:[Ani], B:[Citra]}        → {A:[Ani, Budi], B:[Citra]}
```

**Kenapa tidak `itertools.groupby`?** `groupby` hanya menggabungkan elemen yang
**berurutan**, jadi data harus diurutkan dulu. `kelompokkan` tidak butuh itu.

---

### 7. `jumlahkan(nilai)` · [fplib.py#L146](../fplib.py#L146)
Persis seperti contoh di slide: `sum(map(f, data))` ([baris 157](../fplib.py#L157)).
`map` menghitung nilai tiap elemen, lalu `sum` menjumlahkannya.

**Satu fungsi, tiga aplikasi:**
| Aplikasi | Baris | Fungsi yang dikirim |
|---|---|---|
| Kasir | [kasir_kantin.py#L72](../kasir_kantin.py#L72) | `lambda i: i["harga"] * i["qty"]` |
| Keuangan | [keuangan_pribadi.py#L68](../keuangan_pribadi.py#L68) | `lambda t: t["nominal"]` |
| Nilai | [nilai_mahasiswa.py#L66](../nilai_mahasiswa.py#L66) | `lambda k: k["nilai"] * k["bobot"]` |

Fungsinya sama, yang berbeda hanya cara menghitung nilai yang dikirim.

---

### 8. `rata_rata(nilai)` · [fplib.py#L160](../fplib.py#L160)
Menghitung `sum / len`. **Kasus tepi:** data kosong akan menyebabkan pembagian
dengan nol, jadi dicegah dengan `if angka else 0.0` ([baris 172](../fplib.py#L172)).

**Trik di Presensi** ([presensi_kelas.py#L38](../presensi_kelas.py#L38)):
`rata_rata(lambda c: 100 if c["status"] == "H" else 0)`. Rata-rata dari
nilai 100/0 sama dengan **persentase hadir**. Jadi satu fungsi dipakai untuk dua makna.

---

### 9. `validasi(*aturan)` · [fplib.py#L177](../fplib.py#L177)
**Definisi:** membuat pemeriksa dari pasangan `(syarat, pesan)`. Pemeriksa
mengembalikan **list pesan kesalahan**; list kosong = valid.

**Kenapa mengembalikan list pesan, bukan True/False?** Supaya pengguna tahu
**semua** alasan data salah sekaligus, bukan hanya "salah".

**Pengaman** ([baris 197–201](../fplib.py#L197)): `lolos()` menangkap error
(kolom hilang, tipe salah). Syarat yang error dianggap **gagal**, sehingga
program tidak crash karena data rusak.

**Kode inti** ([baris 203](../fplib.py#L203)):
```python
lambda item: list(map(lambda a: a[1], filter(lambda a: not lolos(a[0], item), aturan)))
```
Dibaca dari dalam: saring aturan yang **tidak lolos**, lalu ambil **pesan**-nya (`a[1]`).

**Pola di aplikasi:** `saring(lambda x: not cek(x))` = data valid;
`saring(lambda x: bool(cek(x)))` = data ditolak. Lihat
[keuangan_pribadi.py#L43](../keuangan_pribadi.py#L43).

---

### 10. `rupiah(angka)` · [fplib.py#L208](../fplib.py#L208)
Satu-satunya fungsi yang **langsung** mengembalikan hasil (teks), karena
tidak butuh aturan tambahan. Tetap murni.

```python
bulat = int(abs(angka) + 0.5)                       # baris 230
tanda = "-" if angka < 0 and bulat else ""          # baris 231
return f"{tanda}Rp{bulat:,}".replace(",", ".")      # baris 232
```
- `abs(angka) + 0.5` lalu `int(...)`: pembulatan **setengah ke atas** (2,5 → 3).
  Ini dipilih karena `round()` bawaan Python memakai *banker's rounding* (2,5 → 2).
- `and bulat`: tanda minus hanya dipasang jika hasil bulatnya bukan 0, supaya
  `rupiah(-0.4)` menjadi `Rp0`, bukan `-Rp0`.
- `:,` memberi pemisah ribuan gaya Inggris (`1,500,000`), lalu `.replace(",", ".")`
  mengubahnya ke gaya Indonesia (`1.500.000`).

---

## Bagian 2 — Alur tiap aplikasi

Semua aplikasi punya tiga bagian: **Data → Logika → Tampilan (`main`)**.

**Kasir Kantin** ([kasir_kantin.py#L61](../kasir_kantin.py#L61))
```
PESANAN ─saring(valid)→ ─ambil(ke_item_keranjang: cari menu)→ ─urutkan(subtotal↓)→ keranjang
keranjang ─jumlahkan(harga×qty)→ total ─rupiah→ tampilan
```

**Presensi Kelas** ([presensi_kelas.py#L54](../presensi_kelas.py#L54))
```
PRESENSI ─kelompokkan(nim)→ ─ambil isi dict→ ─ambil(rekap_satu: saring H + rata_rata)→ rekap
rekap ─saring(persen < 75)→ tidak boleh ujian
```

**Perpustakaan Mini** ([perpustakaan_mini.py#L87](../perpustakaan_mini.py#L87))
```
PEMINJAMAN ─ambil(lengkapi_denda: cari buku)→ ─saring(denda>0)→ ─urutkan(denda↓)→ daftar denda
KATALOG ─urutkan(kategori, judul)→ ─kelompokkan(kategori)→ katalog
PERMINTAAN ─validasi(buku ada, stok, nama)→ disetujui / ditolak
```

**Keuangan Pribadi** ([keuangan_pribadi.py#L63](../keuangan_pribadi.py#L63))
```
TRANSAKSI ─saring(valid)→ ─saring(masuk/keluar)→ ─jumlahkan(nominal)→ saldo
pengeluaran ─kelompokkan(kategori)→ ─ambil(total)→ ─urutkan(total↓)→ per kategori
```

**Nilai Mahasiswa** ([nilai_mahasiswa.py#L80](../nilai_mahasiswa.py#L80))
```
MAHASISWA ─saring(valid)→ ─ambil(nilai akhir + cari huruf)→ ─urutkan(akhir↓)→ peringkat
peringkat ─rata_rata(akhir)→ rata kelas ; ─saring(≥60)→ lulus
```

---

## Bagian 3 — Kemungkinan pertanyaan dosen

| Pertanyaan | Jawaban singkat |
|---|---|
| Kenapa fungsinya mengembalikan fungsi? | Agar bentuknya seragam `f(data)` sehingga bisa dirangkai `pipe`, dan satu "aturan" bisa dipakai ulang di banyak data. |
| Apa itu closure? | Fungsi dalam yang mengingat variabel fungsi luarnya, mis. `f` di `jumlahkan`. |
| Bukti fungsinya murni? | `test_data_asli_tidak_berubah`: data disalin, diproses, dibandingkan. Memakai `sorted`, `{**dict}`, `list + [x]`, bukan `.sort()`/`.append()`. |
| Bedanya `saring` dan `cari`? | `saring` semua yang cocok (list), `cari` yang pertama saja dan berhenti cepat lewat `next`. |
| Kenapa pakai `reduce` di `pipe` & `kelompokkan`? | `reduce` "melipat" daftar menjadi satu hasil langkah demi langkah tanpa variabel yang diubah-ubah. |
| Bagaimana membuktikan tiap fungsi dipakai ≥ 3 aplikasi? | `tools/matriks.py` membaca kode dengan `ast` dan mencatat file + baris; `pytest` gagal jika aturan dilanggar. Hasilnya di MATRIKS.md. |
| Kalau data kosong? | `jumlahkan` → 0, `rata_rata` → 0.0, `cari` → `bawaan`, `kelompokkan` → `{}`. Semua diuji. |
| Kenapa `rupiah` tidak berpola `fungsi()(data)`? | Tidak butuh aturan tambahan; justru karena berbentuk `f(x)`, ia bisa langsung dikirim ke `ambil(rupiah)`. |
| Kenapa ada `round(akhir, 2)` di Nilai? | Pecahan biner bisa membuat 80 menjadi 79.999…, sehingga huruf A bisa turun ke B+. |

---

## Rujukan

- Dokumentasi resmi Python — *Functional Programming HOWTO*: <https://docs.python.org/3/howto/functional.html>
- `functools.reduce`: <https://docs.python.org/3/library/functools.html#functools.reduce>
- Fungsi bawaan `map`, `filter`, `sorted`, `next`, `round`: <https://docs.python.org/3/library/functions.html>
- Stabilitas pengurutan (*Sorting Techniques*): <https://docs.python.org/3/howto/sorting.html>
- Modul `ast`: <https://docs.python.org/3/library/ast.html>
- Dokumentasi pytest: <https://docs.pytest.org/>
