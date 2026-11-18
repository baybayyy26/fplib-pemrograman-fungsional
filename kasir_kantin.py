"""
Aplikasi 1 — Kasir Kantin
Menu, keranjang, dan total belanja.

Fungsi fplib yang dipakai: pipe, ambil, saring, cari, urutkan,
jumlahkan, validasi, rupiah.

Jalankan:  python kasir_kantin.py
"""

from fplib import pipe, ambil, saring, cari, urutkan, jumlahkan, validasi, rupiah

# ---------------------------------------------------------------------------
# Data (tuple agar tidak bisa diubah tanpa sengaja)
# ---------------------------------------------------------------------------
MENU = (
    {"kode": "M01", "nama": "Nasi Goreng", "kategori": "makanan", "harga": 12000},
    {"kode": "M02", "nama": "Mie Ayam", "kategori": "makanan", "harga": 10000},
    {"kode": "M03", "nama": "Ayam Geprek", "kategori": "makanan", "harga": 13000},
    {"kode": "M04", "nama": "Soto Ayam", "kategori": "makanan", "harga": 11000},
    {"kode": "D01", "nama": "Es Teh", "kategori": "minuman", "harga": 3000},
    {"kode": "D02", "nama": "Es Jeruk", "kategori": "minuman", "harga": 4000},
    {"kode": "D03", "nama": "Kopi Susu", "kategori": "minuman", "harga": 6000},
)

# Pesanan yang diketik kasir. Dua baris terakhir sengaja salah
# untuk menunjukkan kerja fungsi validasi.
PESANAN = (
    {"kode": "M01", "qty": 2},
    {"kode": "D01", "qty": 3},
    {"kode": "M03", "qty": 1},
    {"kode": "D03", "qty": 1},
    {"kode": "M02", "qty": 0},  # salah: qty 0
    {"kode": "X99", "qty": 1},  # salah: kode tidak ada di menu
)

UANG_DIBAYAR = 60000


# ---------------------------------------------------------------------------
# Logika (fungsi murni, tanpa print)
# ---------------------------------------------------------------------------
def cari_menu(kode):
    """Cari satu menu berdasarkan kode; None jika tidak ada."""
    return cari(lambda m: m["kode"] == kode)(MENU)


cek_pesanan = validasi(
    (lambda p: cari_menu(p["kode"]) is not None, "kode menu tidak ditemukan"),
    (lambda p: isinstance(p["qty"], int) and p["qty"] > 0, "qty harus bilangan bulat > 0"),
)


def ke_item_keranjang(pesanan):
    """Gabungkan data menu dengan qty pesanan menjadi satu item keranjang."""
    menu = cari_menu(pesanan["kode"])
    return {**menu, "qty": pesanan["qty"], "subtotal": menu["harga"] * pesanan["qty"]}


# Alur: buang pesanan salah -> ubah jadi item keranjang -> urutkan subtotal terbesar
buat_keranjang = pipe(
    saring(lambda p: not cek_pesanan(p)),
    ambil(ke_item_keranjang),
    urutkan("subtotal", menurun=True),
)

pesanan_ditolak = saring(lambda p: bool(cek_pesanan(p)))


def total_belanja(keranjang):
    """Total belanja = jumlah (harga x qty) seluruh item (contoh persis dari slide)."""
    return jumlahkan(lambda i: i["harga"] * i["qty"])(keranjang)


# ---------------------------------------------------------------------------
# Tampilan
# ---------------------------------------------------------------------------
def main():
    print("=" * 52)
    print(" KASIR KANTIN".center(52))
    print("=" * 52)

    print("\nDAFTAR MENU (termurah dulu)")
    baris_menu = ambil(
        lambda m: f"  {m['kode']}  {m['nama']:<14} {m['kategori']:<8} {rupiah(m['harga']):>9}"
    )(urutkan("harga")(MENU))
    print("\n".join(baris_menu))

    ditolak = pesanan_ditolak(PESANAN)
    if ditolak:
        print("\nPESANAN DITOLAK")
        print("\n".join(ambil(
            lambda p: f"  {p['kode']} x{p['qty']}: {', '.join(cek_pesanan(p))}"
        )(ditolak)))

    keranjang = buat_keranjang(PESANAN)
    print("\nKERANJANG (subtotal terbesar dulu)")
    print("\n".join(ambil(
        lambda i: f"  {i['nama']:<14} {i['qty']:>2} x {rupiah(i['harga']):>8} = {rupiah(i['subtotal']):>9}"
    )(keranjang)))

    total = total_belanja(keranjang)
    print("-" * 52)
    print(f"  {'TOTAL':<30}{rupiah(total):>18}")
    print(f"  {'DIBAYAR':<30}{rupiah(UANG_DIBAYAR):>18}")
    if UANG_DIBAYAR >= total:
        print(f"  {'KEMBALIAN':<30}{rupiah(UANG_DIBAYAR - total):>18}")
    else:
        print(f"  {'UANG KURANG':<30}{rupiah(total - UANG_DIBAYAR):>18}")
    print("=" * 52)


if __name__ == "__main__":
    main()
