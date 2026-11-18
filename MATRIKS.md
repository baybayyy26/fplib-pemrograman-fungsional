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
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [61](kasir_kantin.py#L61) |
| Presensi | [`presensi_kelas.py`](presensi_kelas.py) | [54](presensi_kelas.py#L54), [61](presensi_kelas.py#L61) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [87](perpustakaan_mini.py#L87), [94](perpustakaan_mini.py#L94) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [55](keuangan_pribadi.py#L55) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [80](nilai_mahasiswa.py#L80) |

### `ambil`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [63](kasir_kantin.py#L63), [84](kasir_kantin.py#L84), [92](kasir_kantin.py#L92), [98](kasir_kantin.py#L98) |
| Presensi | [`presensi_kelas.py`](presensi_kelas.py) | [57](presensi_kelas.py#L57), [64](presensi_kelas.py#L64), [81](presensi_kelas.py#L81), [90](presensi_kelas.py#L90), [96](presensi_kelas.py#L96) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [88](perpustakaan_mini.py#L88), [118](perpustakaan_mini.py#L118), [127](perpustakaan_mini.py#L127), [136](perpustakaan_mini.py#L136) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [58](keuangan_pribadi.py#L58), [89](keuangan_pribadi.py#L89), [98](keuangan_pribadi.py#L98), [107](keuangan_pribadi.py#L107) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [82](nilai_mahasiswa.py#L82), [98](nilai_mahasiswa.py#L98), [108](nilai_mahasiswa.py#L108), [111](nilai_mahasiswa.py#L111) |

### `saring`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [62](kasir_kantin.py#L62), [67](kasir_kantin.py#L67) |
| Presensi | [`presensi_kelas.py`](presensi_kelas.py) | [39](presensi_kelas.py#L39), [67](presensi_kelas.py#L67) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [61](perpustakaan_mini.py#L61), [67](perpustakaan_mini.py#L67), [89](perpustakaan_mini.py#L89) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [43](keuangan_pribadi.py#L43), [44](keuangan_pribadi.py#L44), [45](keuangan_pribadi.py#L45), [46](keuangan_pribadi.py#L46) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [52](nilai_mahasiswa.py#L52), [81](nilai_mahasiswa.py#L81), [95](nilai_mahasiswa.py#L95), [118](nilai_mahasiswa.py#L118) |

### `cari`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [45](kasir_kantin.py#L45) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [58](perpustakaan_mini.py#L58) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [71](nilai_mahasiswa.py#L71) |

### `urutkan`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [64](kasir_kantin.py#L64), [86](kasir_kantin.py#L86) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [90](perpustakaan_mini.py#L90), [95](perpustakaan_mini.py#L95) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [59](keuangan_pribadi.py#L59), [103](keuangan_pribadi.py#L103) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [83](nilai_mahasiswa.py#L83) |

### `kelompokkan`

| Aplikasi | File | Baris |
|---|---|---|
| Presensi | [`presensi_kelas.py`](presensi_kelas.py) | [55](presensi_kelas.py#L55), [62](presensi_kelas.py#L62) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [96](perpustakaan_mini.py#L96) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [56](keuangan_pribadi.py#L56) |

### `jumlahkan`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [72](kasir_kantin.py#L72) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [51](keuangan_pribadi.py#L51), [67](keuangan_pribadi.py#L67), [68](keuangan_pribadi.py#L68) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [56](nilai_mahasiswa.py#L56), [66](nilai_mahasiswa.py#L66) |

### `rata_rata`

| Aplikasi | File | Baris |
|---|---|---|
| Presensi | [`presensi_kelas.py`](presensi_kelas.py) | [38](presensi_kelas.py#L38), [95](presensi_kelas.py#L95) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [73](keuangan_pribadi.py#L73) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [120](nilai_mahasiswa.py#L120) |

### `validasi`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [48](kasir_kantin.py#L48) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [99](perpustakaan_mini.py#L99) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [37](keuangan_pribadi.py#L37) |
| Nilai | [`nilai_mahasiswa.py`](nilai_mahasiswa.py) | [54](nilai_mahasiswa.py#L54) |

### `rupiah`

| Aplikasi | File | Baris |
|---|---|---|
| Kasir | [`kasir_kantin.py`](kasir_kantin.py) | [85](kasir_kantin.py#L85), [99](kasir_kantin.py#L99), [104](kasir_kantin.py#L104), [105](kasir_kantin.py#L105), [107](kasir_kantin.py#L107), [109](kasir_kantin.py#L109) |
| Perpus | [`perpustakaan_mini.py`](perpustakaan_mini.py) | [126](perpustakaan_mini.py#L126), [130](perpustakaan_mini.py#L130) |
| Keuangan | [`keuangan_pribadi.py`](keuangan_pribadi.py) | [91](keuangan_pribadi.py#L91), [101](keuangan_pribadi.py#L101), [109](keuangan_pribadi.py#L109), [115](keuangan_pribadi.py#L115), [116](keuangan_pribadi.py#L116), [117](keuangan_pribadi.py#L117), [118](keuangan_pribadi.py#L118) |

