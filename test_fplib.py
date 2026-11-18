"""
Pengujian untuk fplib.py dan kelima aplikasi.

Jalankan:  pytest -v
"""

import copy
import doctest
import importlib
import importlib.util
from pathlib import Path

import pytest

import fplib
from fplib import (
    ambil,
    cari,
    jumlahkan,
    kelompokkan,
    pipe,
    rata_rata,
    rupiah,
    saring,
    urutkan,
    validasi,
)

AKAR = Path(__file__).resolve().parent

DATA = (
    {"nama": "Ani", "kelas": "A", "nilai": 78},
    {"nama": "Budi", "kelas": "A", "nilai": 85},
    {"nama": "Citra", "kelas": "B", "nilai": 62},
)


# ---------------------------------------------------------------------------
# pipe
# ---------------------------------------------------------------------------
def test_pipe_menjalankan_dari_kiri_ke_kanan():
    assert pipe(lambda x: x + 1, lambda x: x * 2)(3) == 8  # (3+1)*2, bukan 3*2+1


def test_pipe_tanpa_langkah_mengembalikan_data_apa_adanya():
    assert pipe()("tetap") == "tetap"


def test_pipe_merangkai_fungsi_fplib():
    alur = pipe(saring(lambda m: m["nilai"] >= 70), urutkan("nilai", menurun=True), ambil("nama"))
    assert alur(DATA) == ["Budi", "Ani"]


# ---------------------------------------------------------------------------
# ambil
# ---------------------------------------------------------------------------
def test_ambil_satu_kolom():
    assert ambil("nama")(DATA) == ["Ani", "Budi", "Citra"]


def test_ambil_beberapa_kolom():
    assert ambil("nama", "nilai")(DATA)[0] == {"nama": "Ani", "nilai": 78}


def test_ambil_dengan_fungsi():
    assert ambil(lambda m: m["nilai"] // 10)(DATA) == [7, 8, 6]


def test_ambil_data_kosong():
    assert ambil("nama")([]) == []


def test_ambil_tanpa_argumen_error():
    with pytest.raises(TypeError):
        ambil()


# ---------------------------------------------------------------------------
# saring
# ---------------------------------------------------------------------------
def test_saring_memilih_yang_lolos():
    assert ambil("nama")(saring(lambda m: m["kelas"] == "A")(DATA)) == ["Ani", "Budi"]


def test_saring_tidak_ada_yang_lolos():
    assert saring(lambda m: m["nilai"] > 100)(DATA) == []


# ---------------------------------------------------------------------------
# cari
# ---------------------------------------------------------------------------
def test_cari_mengembalikan_elemen_pertama():
    assert cari(lambda m: m["kelas"] == "A")(DATA)["nama"] == "Ani"


def test_cari_tidak_ketemu_mengembalikan_none():
    assert cari(lambda m: m["nama"] == "Zaki")(DATA) is None


def test_cari_tidak_ketemu_dengan_nilai_bawaan():
    assert cari(lambda m: m["nama"] == "Zaki", bawaan={})(DATA) == {}


# ---------------------------------------------------------------------------
# urutkan
# ---------------------------------------------------------------------------
def test_urutkan_naik_dan_menurun():
    assert ambil("nilai")(urutkan("nilai")(DATA)) == [62, 78, 85]
    assert ambil("nilai")(urutkan("nilai", menurun=True)(DATA)) == [85, 78, 62]


def test_urutkan_stabil_untuk_nilai_sama():
    data = [{"n": "x", "k": 1}, {"n": "y", "k": 0}, {"n": "z", "k": 1}]
    assert ambil("n")(urutkan("k")(data)) == ["y", "x", "z"]


# ---------------------------------------------------------------------------
# kelompokkan
# ---------------------------------------------------------------------------
def test_kelompokkan_per_kunci_dan_urutan_terjaga():
    hasil = kelompokkan("kelas")(DATA)
    assert list(hasil) == ["A", "B"]
    assert ambil("nama")(hasil["A"]) == ["Ani", "Budi"]


def test_kelompokkan_dengan_fungsi():
    hasil = kelompokkan(lambda m: "lulus" if m["nilai"] >= 70 else "tidak")(DATA)
    assert {k: len(v) for k, v in hasil.items()} == {"lulus": 2, "tidak": 1}


def test_kelompokkan_data_kosong():
    assert kelompokkan("kelas")([]) == {}


# ---------------------------------------------------------------------------
# jumlahkan — tiga contoh persis dari slide
# ---------------------------------------------------------------------------
def test_jumlahkan_kasir_total_belanja():
    keranjang = [{"harga": 12000, "qty": 2}, {"harga": 3000, "qty": 3}]
    assert jumlahkan(lambda i: i["harga"] * i["qty"])(keranjang) == 33000


def test_jumlahkan_keuangan_total_pengeluaran():
    pengeluaran = [{"nominal": 25000}, {"nominal": 15000}]
    assert jumlahkan(lambda t: t["nominal"])(pengeluaran) == 40000


def test_jumlahkan_nilai_akhir_berbobot():
    komponen = [{"nilai": 80, "bobot": 0.3}, {"nilai": 70, "bobot": 0.3}, {"nilai": 90, "bobot": 0.4}]
    assert jumlahkan(lambda k: k["nilai"] * k["bobot"])(komponen) == pytest.approx(81.0)


def test_jumlahkan_kosong_nol():
    assert jumlahkan("nilai")([]) == 0


# ---------------------------------------------------------------------------
# rata_rata
# ---------------------------------------------------------------------------
def test_rata_rata_biasa():
    assert rata_rata("nilai")(DATA) == pytest.approx(75.0)


def test_rata_rata_kosong_tidak_error():
    assert rata_rata("nilai")([]) == 0.0


# ---------------------------------------------------------------------------
# validasi
# ---------------------------------------------------------------------------
cek = validasi(
    (lambda x: x["qty"] > 0, "qty harus > 0"),
    (lambda x: x["harga"] >= 0, "harga negatif"),
)


def test_validasi_data_benar_tanpa_pesan():
    assert cek({"qty": 1, "harga": 0}) == []


def test_validasi_mengumpulkan_semua_pesan():
    assert cek({"qty": 0, "harga": -5}) == ["qty harus > 0", "harga negatif"]


def test_validasi_kolom_hilang_dianggap_gagal_bukan_crash():
    assert cek({}) == ["qty harus > 0", "harga negatif"]


# ---------------------------------------------------------------------------
# rupiah
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "angka, harapan",
    [
        (0, "Rp0"),
        (500, "Rp500"),
        (12500, "Rp12.500"),
        (1500000, "Rp1.500.000"),
        (-7500, "-Rp7.500"),
        (2.5, "Rp3"),
        (1234567.6, "Rp1.234.568"),
    ],
)
def test_rupiah(angka, harapan):
    assert rupiah(angka) == harapan


# ---------------------------------------------------------------------------
# Sifat fungsional: data asli tidak pernah berubah
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "fungsi",
    [
        ambil("nama"),
        saring(lambda m: m["nilai"] > 70),
        cari(lambda m: m["kelas"] == "B"),
        urutkan("nilai", menurun=True),
        kelompokkan("kelas"),
        jumlahkan("nilai"),
        rata_rata("nilai"),
        pipe(urutkan("nama"), ambil("nilai")),
    ],
)
def test_data_asli_tidak_berubah(fungsi):
    data = [dict(d) for d in DATA]
    salinan = copy.deepcopy(data)
    fungsi(data)
    assert data == salinan


def test_hasil_sama_jika_dipanggil_berulang():
    alur = pipe(saring(lambda m: m["nilai"] >= 70), ambil("nama"))
    assert alur(DATA) == alur(DATA)


def test_contoh_di_docstring_benar():
    hasil = doctest.testmod(fplib, verbose=False)
    assert hasil.failed == 0 and hasil.attempted > 0


# ---------------------------------------------------------------------------
# Aturan tugas: setiap fungsi dipakai minimal 3 dari 5 aplikasi
# ---------------------------------------------------------------------------
def _muat_pemindai():
    spec = importlib.util.spec_from_file_location("matriks", AKAR / "tools" / "matriks.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def test_setiap_fungsi_dipakai_minimal_3_aplikasi_sesuai_slide():
    m = _muat_pemindai()
    daftar, hasil, masalah = m.bangun_matriks()
    assert m.periksa(daftar, hasil, masalah) == []


def test_semua_fungsi_di_all_benar_benar_ada():
    for nama in fplib.__all__:
        assert callable(getattr(fplib, nama))


# ---------------------------------------------------------------------------
# Kelima aplikasi bisa dijalankan dan hasil kuncinya benar
# ---------------------------------------------------------------------------
APLIKASI = ["kasir_kantin", "presensi_kelas", "perpustakaan_mini", "keuangan_pribadi", "nilai_mahasiswa"]


@pytest.mark.parametrize("nama_modul", APLIKASI)
def test_aplikasi_berjalan_tanpa_error(nama_modul, capsys):
    importlib.import_module(nama_modul).main()
    assert "=" * 20 in capsys.readouterr().out


def test_kasir_total_belanja():
    import kasir_kantin as k

    keranjang = k.buat_keranjang(k.PESANAN)
    assert k.total_belanja(keranjang) == 52000
    assert len(k.pesanan_ditolak(k.PESANAN)) == 2


def test_presensi_rekap():
    import presensi_kelas as p

    rekap = p.rekap_per_mahasiswa(p.PRESENSI)
    assert ambil("nama")(p.tidak_memenuhi_syarat(rekap)) == ["Citra", "Eka"]


def test_perpustakaan_denda():
    import perpustakaan_mini as p

    denda = p.daftar_denda(p.PEMINJAMAN)
    assert ambil("id", "denda")(denda)[0] == {"id": "P02", "denda": 8000}
    assert p.cek_permintaan({"kode": "B05", "peminjam": "Fajar"}) == []
    assert p.cek_permintaan({"kode": "B99", "peminjam": "Hana"}) == ["kode buku tidak ditemukan"]


def test_keuangan_ringkasan():
    import keuangan_pribadi as k

    r = k.ringkasan(k.transaksi_valid(k.TRANSAKSI))
    assert (r["masuk"], r["keluar"], r["saldo"]) == (1900000, 312000, 1588000)
    assert r["per_kategori"][0]["kategori"] == "Internet"


def test_nilai_peringkat():
    import nilai_mahasiswa as n

    peringkat = n.buat_peringkat(n.MAHASISWA)
    assert ambil("nama")(peringkat)[0] == "Citra"
    assert len(peringkat) == 5  # Fajar ditolak validasi
    assert n.huruf_dari(80.0) == "A"
