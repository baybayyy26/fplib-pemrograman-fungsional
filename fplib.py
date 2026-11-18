"""
fplib — library fungsional kecil untuk tugas Pemrograman Fungsional.

Semua fungsi di sini ditulis dengan gaya fungsional:

1. Murni (pure): tidak mengubah data masukan, tidak membaca/menulis
   variabel global, hasil hanya ditentukan oleh argumen.
2. Higher-order: sebagian besar fungsi MENERIMA fungsi (misalnya lambda)
   dan MENGEMBALIKAN fungsi baru yang menunggu data.
3. Bisa dirangkai: karena fungsi yang dikembalikan selalu berbentuk
   ``f(data) -> hasil``, semuanya bisa disusun dengan ``pipe``.

Pola pemakaian (sama seperti contoh ``jumlahkan`` di slide):

    >>> keranjang = [{"harga": 5000, "qty": 2}, {"harga": 3000, "qty": 1}]
    >>> jumlahkan(lambda i: i["harga"] * i["qty"])(keranjang)
    13000

Parameter ``kunci``/``nilai`` di banyak fungsi boleh berupa:
- fungsi (misalnya ``lambda m: m["nilai"] * 2``), atau
- nama kolom (misalnya ``"nilai"``) — otomatis diubah menjadi
  ``lambda item: item["nilai"]``.
"""

from functools import reduce

__all__ = [
    "pipe",
    "ambil",
    "saring",
    "cari",
    "urutkan",
    "kelompokkan",
    "jumlahkan",
    "rata_rata",
    "validasi",
    "rupiah",
]


def _ke_fungsi(kunci):
    """Ubah nama kolom menjadi fungsi pengambil nilai; fungsi dibiarkan apa adanya.

    >>> _ke_fungsi("nama")({"nama": "Ani"})
    'Ani'
    >>> _ke_fungsi(len)("abc")
    3
    """
    if callable(kunci):
        return kunci
    return lambda item: item[kunci]


def pipe(*langkah):
    """Rangkai beberapa fungsi menjadi satu alur, dijalankan dari kiri ke kanan.

    ``pipe(f, g, h)(data)`` sama dengan ``h(g(f(data)))``.
    Tanpa langkah sama sekali, ``pipe()`` mengembalikan data apa adanya.

    >>> tambah_satu = lambda x: x + 1
    >>> kali_dua = lambda x: x * 2
    >>> pipe(tambah_satu, kali_dua)(3)
    8
    >>> pipe()(5)
    5
    """
    return lambda data: reduce(lambda hasil, f: f(hasil), langkah, data)


def ambil(*kunci):
    """Ambil/ubah setiap elemen data (versi fungsional dari ``map``).

    - ``ambil("nama")``          -> daftar nilai kolom "nama"
    - ``ambil("nama", "nilai")`` -> daftar dict yang hanya berisi kolom itu
      (mode beberapa kunci hanya menerima NAMA KOLOM, bukan fungsi)
    - ``ambil(fungsi)``          -> daftar hasil fungsi untuk tiap elemen

    >>> data = [{"nama": "Ani", "nilai": 78}, {"nama": "Budi", "nilai": 85}]
    >>> ambil("nama")(data)
    ['Ani', 'Budi']
    >>> ambil("nama", "nilai")(data)
    [{'nama': 'Ani', 'nilai': 78}, {'nama': 'Budi', 'nilai': 85}]
    >>> ambil(lambda m: m["nilai"] + 5)(data)
    [83, 90]
    """
    if len(kunci) == 0:
        raise TypeError("ambil() butuh minimal satu kunci atau fungsi")
    if len(kunci) == 1:
        ubah = _ke_fungsi(kunci[0])
    else:
        ubah = lambda item: {k: item[k] for k in kunci}
    return lambda data: list(map(ubah, data))


def saring(predikat):
    """Ambil hanya elemen yang memenuhi syarat (versi fungsional dari ``filter``).

    >>> saring(lambda x: x >= 60)([78, 85, 55, 90])
    [78, 85, 90]
    """
    return lambda data: list(filter(predikat, data))


def cari(predikat, bawaan=None):
    """Kembalikan elemen PERTAMA yang memenuhi syarat, atau ``bawaan`` jika tidak ada.

    >>> menu = [{"kode": "M01", "nama": "Nasi Goreng"}, {"kode": "M02", "nama": "Es Teh"}]
    >>> cari(lambda m: m["kode"] == "M02")(menu)["nama"]
    'Es Teh'
    >>> cari(lambda m: m["kode"] == "X99")(menu) is None
    True
    """
    return lambda data: next(filter(predikat, data), bawaan)


def urutkan(kunci, menurun=False):
    """Urutkan data berdasarkan kunci tanpa mengubah data asli (memakai ``sorted``).

    >>> data = [{"nama": "Ani", "nilai": 78}, {"nama": "Budi", "nilai": 85}]
    >>> ambil("nama")(urutkan("nilai", menurun=True)(data))
    ['Budi', 'Ani']
    """
    return lambda data: sorted(data, key=_ke_fungsi(kunci), reverse=menurun)


def kelompokkan(kunci):
    """Kelompokkan data menjadi ``{kunci: [elemen, ...]}``, urutan kemunculan tetap.

    Ditulis dengan ``reduce``: setiap langkah membuat dict BARU,
    bukan mengubah dict lama.

    >>> data = [{"kelas": "A", "nama": "Ani"}, {"kelas": "B", "nama": "Citra"},
    ...         {"kelas": "A", "nama": "Budi"}]
    >>> {k: ambil("nama")(v) for k, v in kelompokkan("kelas")(data).items()}
    {'A': ['Ani', 'Budi'], 'B': ['Citra']}
    """
    ambil_kunci = _ke_fungsi(kunci)

    def tambahkan(kelompok, item):
        k = ambil_kunci(item)
        return {**kelompok, k: kelompok.get(k, []) + [item]}

    return lambda data: reduce(tambahkan, data, {})


def jumlahkan(nilai):
    """Jumlahkan hasil fungsi ``nilai`` untuk setiap elemen (sesuai contoh di slide).

    >>> jumlahkan(lambda i: i["harga"] * i["qty"])([{"harga": 5000, "qty": 2}])
    10000
    >>> jumlahkan("nominal")([{"nominal": 20000}, {"nominal": 15000}])
    35000
    >>> jumlahkan("nominal")([])
    0
    """
    f = _ke_fungsi(nilai)
    return lambda data: sum(map(f, data))


def rata_rata(nilai):
    """Hitung rata-rata hasil fungsi ``nilai``; data kosong menghasilkan 0.0.

    >>> rata_rata("nilai")([{"nilai": 78}, {"nilai": 85}, {"nilai": 62}])
    75.0
    >>> rata_rata("nilai")([])
    0.0
    """
    f = _ke_fungsi(nilai)

    def hitung(data):
        angka = list(map(f, data))
        return sum(angka) / len(angka) if angka else 0.0

    return hitung


def validasi(*aturan):
    """Buat pemeriksa data dari pasangan ``(syarat, pesan_kesalahan)``.

    Fungsi yang dihasilkan menerima SATU elemen dan mengembalikan daftar
    pesan kesalahan. Daftar kosong berarti data valid. Syarat yang
    error (misalnya kolom tidak ada) dianggap gagal, bukan membuat
    program berhenti.

    >>> cek = validasi(
    ...     (lambda x: x["qty"] > 0, "qty harus lebih dari 0"),
    ...     (lambda x: x["harga"] >= 0, "harga tidak boleh negatif"),
    ... )
    >>> cek({"qty": 2, "harga": 5000})
    []
    >>> cek({"qty": 0, "harga": -1})
    ['qty harus lebih dari 0', 'harga tidak boleh negatif']
    >>> cek({"harga": 5000})
    ['qty harus lebih dari 0']
    """

    def lolos(syarat, item):
        try:
            return bool(syarat(item))
        except (KeyError, IndexError, TypeError, ValueError, AttributeError):
            return False

    return lambda item: list(
        map(lambda a: a[1], filter(lambda a: not lolos(a[0], item), aturan))
    )


def rupiah(angka):
    """Format angka menjadi teks Rupiah dengan pemisah titik, dibulatkan ke rupiah terdekat.

    Berbeda dari fungsi lain, ``rupiah`` langsung mengembalikan teks,
    sehingga bisa langsung dioper ke fungsi lain, misalnya ``ambil(rupiah)``.

    >>> rupiah(12500)
    'Rp12.500'
    >>> rupiah(0)
    'Rp0'
    >>> rupiah(-7500)
    '-Rp7.500'
    >>> rupiah(1234567.6)
    'Rp1.234.568'
    >>> rupiah(2.5)
    'Rp3'
    >>> rupiah(-0.4)
    'Rp0'

    Catatan: dibulatkan "setengah ke atas" (2,5 -> 3), bukan memakai
    ``round()`` bawaan Python yang membulatkan 2,5 -> 2 (banker's rounding).
    """
    bulat = int(abs(angka) + 0.5)
    tanda = "-" if angka < 0 and bulat else ""
    return f"{tanda}Rp{bulat:,}".replace(",", ".")
