# Matriks fungsi × aplikasi

> File ini dibuat otomatis oleh `python tools/matriks.py --tulis`.
> Jangan diedit manual — jalankan ulang perintah itu setelah kode berubah.

| Fungsi | Kasir | Presensi | Perpus | Keuangan | Nilai | Jumlah |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `pipe` | ✓ | ✓ | ✓ | ✓ | ✓ | **5** |
| `ambil` | ✓ | ✓ | ✓ | ✓ | ✓ | **5** |
| `saring` | ✓ | ✓ | ✓ | ✓ | ✓ | **5** |
| `cari` | ✓ |  | ✓ |  | ✓ | **3** |
| `urutkan` | ✓ |  | ✓ | ✓ | ✓ | **4** |
| `kelompokkan` |  | ✓ | ✓ | ✓ |  | **3** |
| `jumlahkan` | ✓ |  |  | ✓ | ✓ | **3** |
| `rata_rata` |  | ✓ |  | ✓ | ✓ | **3** |
| `validasi` | ✓ |  | ✓ | ✓ | ✓ | **4** |
| `rupiah` | ✓ |  | ✓ | ✓ |  | **3** |

Setiap baris minimal 3 centang. Rincian file dan baris pemanggilan di bawah
(klik nomor baris untuk langsung melompat ke kodenya di GitHub).

## Bukti: file dan baris pemanggilan

### `pipe`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [64](kasir_kantin.py#L64) |
| Presensi | [`presensi_kelas.py`](presensi_kelas.py) | [57](presensi_kelas.py#L57), [64](presensi_kelas.py#L64) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [89](perpustakaan_mini.py#L89), [96](perpustakaan_mini.py#L96) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [58](keuangan_pribadi.py#L58) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [83](nilai_mahasiswa.py#L83) |

### `ambil`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [66](kasir_kantin.py#L66), [87](kasir_kantin.py#L87), [95](kasir_kantin.py#L95), [101](kasir_kantin.py#L101), [132](kasir_kantin.py#L132) |
| Presensi | [`presensi_kelas.py`](presensi_kelas.py) | [60](presensi_kelas.py#L60), [67](presensi_kelas.py#L67), [84](presensi_kelas.py#L84), [93](presensi_kelas.py#L93), [99](presensi_kelas.py#L99), [112](presensi_kelas.py#L112) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [90](perpustakaan_mini.py#L90), [120](perpustakaan_mini.py#L120), [129](perpustakaan_mini.py#L129), [138](perpustakaan_mini.py#L138), [162](perpustakaan_mini.py#L162) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [61](keuangan_pribadi.py#L61), [92](keuangan_pribadi.py#L92), [101](keuangan_pribadi.py#L101), [110](keuangan_pribadi.py#L110) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [85](nilai_mahasiswa.py#L85), [101](nilai_mahasiswa.py#L101), [111](nilai_mahasiswa.py#L111), [114](nilai_mahasiswa.py#L114), [149](nilai_mahasiswa.py#L149) |

### `saring`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [65](kasir_kantin.py#L65), [70](kasir_kantin.py#L70) |
| Presensi | [`presensi_kelas.py`](presensi_kelas.py) | [42](presensi_kelas.py#L42), [70](presensi_kelas.py#L70) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [63](perpustakaan_mini.py#L63), [69](perpustakaan_mini.py#L69), [91](perpustakaan_mini.py#L91) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [46](keuangan_pribadi.py#L46), [47](keuangan_pribadi.py#L47), [48](keuangan_pribadi.py#L48), [49](keuangan_pribadi.py#L49) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [55](nilai_mahasiswa.py#L55), [84](nilai_mahasiswa.py#L84), [98](nilai_mahasiswa.py#L98), [121](nilai_mahasiswa.py#L121) |

### `cari`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [48](kasir_kantin.py#L48) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [60](perpustakaan_mini.py#L60) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [74](nilai_mahasiswa.py#L74) |

### `urutkan`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [67](kasir_kantin.py#L67), [89](kasir_kantin.py#L89) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [92](perpustakaan_mini.py#L92), [97](perpustakaan_mini.py#L97) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [62](keuangan_pribadi.py#L62), [106](keuangan_pribadi.py#L106) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [86](nilai_mahasiswa.py#L86) |

### `kelompokkan`

| Aplikasi | File | Baris |
|---|---|---|
| Presensi | [`presensi_kelas.py`](presensi_kelas.py) | [58](presensi_kelas.py#L58), [65](presensi_kelas.py#L65) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [98](perpustakaan_mini.py#L98) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [59](keuangan_pribadi.py#L59) |

### `jumlahkan`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [75](kasir_kantin.py#L75) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [54](keuangan_pribadi.py#L54), [70](keuangan_pribadi.py#L70), [71](keuangan_pribadi.py#L71) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [59](nilai_mahasiswa.py#L59), [69](nilai_mahasiswa.py#L69) |

### `rata_rata`

| Aplikasi | File | Baris |
|---|---|---|
| Presensi | [`presensi_kelas.py`](presensi_kelas.py) | [41](presensi_kelas.py#L41), [98](presensi_kelas.py#L98) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [76](keuangan_pribadi.py#L76) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [123](nilai_mahasiswa.py#L123) |

### `validasi`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [51](kasir_kantin.py#L51) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [101](perpustakaan_mini.py#L101) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [40](keuangan_pribadi.py#L40) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [57](nilai_mahasiswa.py#L57) |

### `rupiah`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [88](kasir_kantin.py#L88), [102](kasir_kantin.py#L102), [107](kasir_kantin.py#L107), [108](kasir_kantin.py#L108), [110](kasir_kantin.py#L110), [112](kasir_kantin.py#L112) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [128](perpustakaan_mini.py#L128), [132](perpustakaan_mini.py#L132) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [94](keuangan_pribadi.py#L94), [104](keuangan_pribadi.py#L104), [112](keuangan_pribadi.py#L112), [118](keuangan_pribadi.py#L118), [119](keuangan_pribadi.py#L119), [120](keuangan_pribadi.py#L120), [121](keuangan_pribadi.py#L121) |

