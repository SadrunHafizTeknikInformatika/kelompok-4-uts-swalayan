import unittest
from toko_swalayan import (
    Makanan, Minuman, KebutuhanRT,
    Transaksi, TokoSwalayan
)


class TestEnkapsulasi(unittest.TestCase):
    """Pengujian enkapsulasi dan kontrol akses data."""

    def setUp(self):
        self.mie = Makanan("Indomie Goreng", 3500, 2500, 100, "2026-12-01")
        self.air = Minuman("Aqua 600ml", 5000, 3000, 50, 600)

    def test_stok_tidak_bisa_negatif(self):
        """Stok tidak bisa diset ke nilai negatif."""
        with self.assertRaises(ValueError):
            self.mie.stok = -1

    def test_harga_tidak_bisa_nol(self):
        """Harga jual tidak bisa 0 atau negatif."""
        with self.assertRaises(ValueError):
            self.mie.harga_jual = 0

    def test_harga_modal_butuh_kode_admin(self):
        """Harga modal tidak bisa diakses tanpa kode admin yang benar."""
        with self.assertRaises(PermissionError):
            self.mie.get_harga_modal("SALAH")

    def test_harga_modal_dengan_kode_benar(self):
        """Harga modal bisa diakses dengan kode admin yang benar."""
        modal = self.mie.get_harga_modal("ADMIN123")
        self.assertEqual(modal, 2500)

    def test_atribut_stok_name_mangling(self):
        """Atribut stok dengan name mangling tidak bisa diakses langsung."""
        with self.assertRaises(AttributeError):
            _ = self.mie.__stok  # harus gagal


class TestTransaksi(unittest.TestCase):
    """Pengujian transaksi penjualan."""

    def setUp(self):
        self.sabun = KebutuhanRT("Sabun Lifebuoy", 8000, 5500, 20, "Lifebuoy")
        self.teh = Minuman("Teh Botol", 6000, 4000, 40, 350)

    def test_stok_berkurang_setelah_transaksi(self):
        """Stok barang berkurang sesuai jumlah yang dibeli."""
        stok_awal = self.sabun.stok
        trx = Transaksi("Pelanggan A")
        trx.tambah_item(self.sabun, 5)
        self.assertEqual(self.sabun.stok, stok_awal - 5)

    def test_total_transaksi_benar(self):
        """Total transaksi dihitung dengan benar."""
        trx = Transaksi("Pelanggan B")
        trx.tambah_item(self.sabun, 2)   # 2 x 8000 = 16000
        trx.tambah_item(self.teh, 3)     # 3 x 6000 = 18000
        self.assertEqual(trx.total, 34000)

    def test_stok_tidak_cukup(self):
        """Transaksi gagal jika stok tidak mencukupi."""
        trx = Transaksi("Pelanggan C")
        with self.assertRaises(ValueError):
            trx.tambah_item(self.sabun, 999)  # stok hanya 20

    def test_tidak_bisa_tambah_item_setelah_selesai(self):
        """Tidak bisa menambah item setelah transaksi selesai."""
        trx = Transaksi("Pelanggan D")
        trx.tambah_item(self.sabun, 1)
        trx.selesaikan()
        with self.assertRaises(RuntimeError):
            trx.tambah_item(self.teh, 1)

    def test_id_transaksi_unik(self):
        """Setiap transaksi memiliki ID yang berbeda."""
        trx1 = Transaksi("A")
        trx2 = Transaksi("B")
        self.assertNotEqual(trx1.id, trx2.id)

    def test_kurangi_stok_jumlah_nol(self):
        """Pengurangan stok dengan jumlah 0 harus gagal."""
        with self.assertRaises(ValueError):
            self.sabun.kurangi_stok(0)


class TestLaporan(unittest.TestCase):
    """Pengujian laporan stok dan transaksi."""

    def setUp(self):
        self.toko = TokoSwalayan("Toko Test")
        self.roti = Makanan("Roti Tawar", 12000, 8000, 30, "2025-06-15")
        self.aqua = Minuman("Aqua 600ml", 5000, 3000, 10, 600)
        self.toko.tambah_barang(self.roti)
        self.toko.tambah_barang(self.aqua)

    def test_barang_terdaftar_di_toko(self):
        """Barang yang ditambahkan tercatat di daftar barang toko."""
        self.assertEqual(len(self.toko.daftar_barang), 2)

    def test_cari_barang_berhasil(self):
        """Pencarian barang berdasarkan nama berhasil."""
        b = self.toko.cari_barang("Roti Tawar")
        self.assertEqual(b.nama, "Roti Tawar")

    def test_cari_barang_tidak_ada(self):
        """Pencarian barang yang tidak ada menghasilkan ValueError."""
        with self.assertRaises(ValueError):
            self.toko.cari_barang("Barang Ajaib")

    def test_riwayat_transaksi_tercatat(self):
        """Transaksi yang dibuat tercatat di riwayat toko."""
        trx = self.toko.buat_transaksi("Andi")
        trx.tambah_item(self.roti, 2)
        trx.selesaikan()
        self.assertEqual(len(self.toko.riwayat_transaksi), 1)
        self.assertEqual(self.toko.riwayat_transaksi[0].total, 24000)

    def test_stok_setelah_beberapa_transaksi(self):
        """Stok barang berkurang secara akumulatif dari beberapa transaksi."""
        trx1 = self.toko.buat_transaksi("Pelanggan 1")
        trx1.tambah_item(self.aqua, 3)
        trx1.selesaikan()

        trx2 = self.toko.buat_transaksi("Pelanggan 2")
        trx2.tambah_item(self.aqua, 4)
        trx2.selesaikan()

        self.assertEqual(self.aqua.stok, 3)  # 10 - 3 - 4 = 3

    def test_keuntungan_per_item(self):
        """Keuntungan per item dihitung dengan benar."""
        keuntungan = self.roti.hitung_keuntungan("ADMIN123")
        self.assertEqual(keuntungan, 4000)  # 12000 - 8000


if __name__ == "__main__":
    unittest.main(verbosity=2)
