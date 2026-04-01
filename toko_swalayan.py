from abc import ABC, abstractmethod
from datetime import datetime



class LogMixin:
    """Mixin untuk mencatat aktivitas sistem."""

    def log(self, pesan: str):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOG {waktu}] {pesan}")


class LaporanMixin:
    """Mixin untuk mencetak laporan."""

    def cetak_garis(self, panjang: int = 50):
        print("=" * panjang)

    def cetak_judul(self, judul: str):
        self.cetak_garis()
        print(f"  {judul}")
        self.cetak_garis()


class Barang(ABC):
    """Kelas abstrak sebagai antarmuka dasar untuk semua jenis barang."""

    def __init__(self, nama: str, harga_jual: float, harga_modal: float, stok: int, kategori: str):
        self._nama = nama
        self._harga_jual = harga_jual
        self.__harga_modal = harga_modal   
        self.__stok = stok                 
        self._kategori = kategori

    
    @property
    def nama(self):
        return self._nama

    @property
    def harga_jual(self):
        return self._harga_jual

    @harga_jual.setter
    def harga_jual(self, nilai: float):
        if nilai <= 0:
            raise ValueError("Harga jual harus lebih dari 0.")
        self._harga_jual = nilai

    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, nilai: int):
        if nilai < 0:
            raise ValueError("Stok tidak boleh negatif.")
        self.__stok = nilai

    @property
    def kategori(self):
        return self._kategori

    def get_harga_modal(self, kode_admin: str) -> float:
        """Harga modal hanya bisa diakses dengan kode admin."""
        if kode_admin == "ADMIN123":
            return self.__harga_modal
        raise PermissionError("Akses ditolak: kode admin salah.")

    def kurangi_stok(self, jumlah: int):
        if jumlah <= 0:
            raise ValueError("Jumlah harus lebih dari 0.")
        if jumlah > self.__stok:
            raise ValueError(f"Stok '{self._nama}' tidak mencukupi. Stok saat ini: {self.__stok}.")
        self.__stok -= jumlah

    def tambah_stok(self, jumlah: int):
        if jumlah <= 0:
            raise ValueError("Jumlah tambah stok harus lebih dari 0.")
        self.__stok += jumlah

    
    @abstractmethod
    def info(self) -> str:
        """Menampilkan informasi barang."""
        pass

    @abstractmethod
    def hitung_keuntungan(self, kode_admin: str) -> float:
        """Menghitung keuntungan per item."""
        pass

    def __str__(self):
        return self.info()


class Makanan(Barang, LogMixin):
    def __init__(self, nama, harga_jual, harga_modal, stok, tanggal_kedaluwarsa: str):
        super().__init__(nama, harga_jual, harga_modal, stok, "Makanan")
        self._tanggal_kedaluwarsa = tanggal_kedaluwarsa

    def info(self) -> str:
        return (f"[{self._kategori}] {self._nama} | "
                f"Harga: Rp{self._harga_jual:,.0f} | "
                f"Stok: {self.stok} | "
                f"Kedaluwarsa: {self._tanggal_kedaluwarsa}")

    def hitung_keuntungan(self, kode_admin: str) -> float:
        return self._harga_jual - self.get_harga_modal(kode_admin)


class Minuman(Barang, LogMixin):
    def __init__(self, nama, harga_jual, harga_modal, stok, volume_ml: int):
        super().__init__(nama, harga_jual, harga_modal, stok, "Minuman")
        self._volume_ml = volume_ml

    def info(self) -> str:
        return (f"[{self._kategori}] {self._nama} | "
                f"Harga: Rp{self._harga_jual:,.0f} | "
                f"Stok: {self.stok} | "
                f"Volume: {self._volume_ml}ml")

    def hitung_keuntungan(self, kode_admin: str) -> float:
        return self._harga_jual - self.get_harga_modal(kode_admin)


class KebutuhanRT(Barang, LogMixin):
    def __init__(self, nama, harga_jual, harga_modal, stok, merek: str):
        super().__init__(nama, harga_jual, harga_modal, stok, "Kebutuhan Rumah Tangga")
        self._merek = merek

    def info(self) -> str:
        return (f"[{self._kategori}] {self._nama} ({self._merek}) | "
                f"Harga: Rp{self._harga_jual:,.0f} | "
                f"Stok: {self.stok}")

    def hitung_keuntungan(self, kode_admin: str) -> float:
        return self._harga_jual - self.get_harga_modal(kode_admin)


class ItemTransaksi:
    def __init__(self, barang: Barang, jumlah: int):
        self._barang = barang
        self._jumlah = jumlah
        self._subtotal = barang.harga_jual * jumlah

    @property
    def barang(self):
        return self._barang

    @property
    def jumlah(self):
        return self._jumlah

    @property
    def subtotal(self):
        return self._subtotal

    def __str__(self):
        return (f"  {self._barang.nama} x{self._jumlah} "
                f"@ Rp{self._barang.harga_jual:,.0f} = Rp{self._subtotal:,.0f}")


class Transaksi(LogMixin):
    _counter = 0

    def __init__(self, nama_pelanggan: str):
        Transaksi._counter += 1
        self.__id = f"TRX{Transaksi._counter:04d}"
        self._nama_pelanggan = nama_pelanggan
        self._item_list: list[ItemTransaksi] = []
        self._waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__total = 0.0
        self._selesai = False

    @property
    def id(self):
        return self.__id

    @property
    def total(self):
        return self.__total

    @property
    def item_list(self):
        return self._item_list

    @property
    def nama_pelanggan(self):
        return self._nama_pelanggan

    @property
    def waktu(self):
        return self._waktu

    def tambah_item(self, barang: Barang, jumlah: int):
        if self._selesai:
            raise RuntimeError("Transaksi sudah selesai, tidak bisa menambah item.")
        barang.kurangi_stok(jumlah)
        item = ItemTransaksi(barang, jumlah)
        self._item_list.append(item)
        self.__total += item.subtotal
        self.log(f"Ditambahkan: {barang.nama} x{jumlah}")

    def selesaikan(self):
        self._selesai = True
        self.log(f"Transaksi {self.__id} selesai. Total: Rp{self.__total:,.0f}")

    def struk(self) -> str:
        baris = [
            "=" * 40,
            f"  TOKO SWALAYAN SEJAHTERA",
            "=" * 40,
            f"  ID       : {self.__id}",
            f"  Pelanggan: {self._nama_pelanggan}",
            f"  Waktu    : {self._waktu}",
            "-" * 40,
        ]
        for item in self._item_list:
            baris.append(str(item))
        baris += [
            "-" * 40,
            f"  TOTAL    : Rp{self.__total:,.0f}",
            "=" * 40,
        ]
        return "\n".join(baris)


class TokoSwalayan(LogMixin, LaporanMixin):
    def __init__(self, nama_toko: str):
        self._nama_toko = nama_toko
        self.__daftar_barang: list[Barang] = []
        self.__riwayat_transaksi: list[Transaksi] = []

    def tambah_barang(self, barang: Barang):
        self.__daftar_barang.append(barang)
        self.log(f"Barang '{barang.nama}' ditambahkan ke toko.")

    def cari_barang(self, nama: str) -> Barang:
        for b in self.__daftar_barang:
            if b.nama.lower() == nama.lower():
                return b
        raise ValueError(f"Barang '{nama}' tidak ditemukan.")

    def buat_transaksi(self, nama_pelanggan: str) -> Transaksi:
        trx = Transaksi(nama_pelanggan)
        self.__riwayat_transaksi.append(trx)
        return trx

    def laporan_stok(self):
        self.cetak_judul(f"LAPORAN STOK BARANG - {self._nama_toko}")
        for b in self.__daftar_barang:
            status = "⚠ HABIS" if b.stok == 0 else ("⚠ MENIPIS" if b.stok < 5 else "✓")
            print(f"  {b.nama:<25} Stok: {b.stok:>4}  {status}")
        self.cetak_garis()

    def laporan_transaksi(self):
        self.cetak_judul(f"LAPORAN TRANSAKSI - {self._nama_toko}")
        total_pendapatan = 0.0
        for trx in self.__riwayat_transaksi:
            print(f"  {trx.id} | {trx.nama_pelanggan:<20} | Rp{trx.total:>10,.0f}")
            total_pendapatan += trx.total
        self.cetak_garis()
        print(f"  Total Pendapatan: Rp{total_pendapatan:,.0f}")
        self.cetak_garis()

    @property
    def daftar_barang(self):
        return self.__daftar_barang

    @property
    def riwayat_transaksi(self):
        return self.__riwayat_transaksi


if __name__ == "__main__":
    toko = TokoSwalayan("Swalayan Sejahtera")

    # Tambah barang
    toko.tambah_barang(Makanan("Indomie Goreng", 3500, 2500, 100, "2026-12-01"))
    toko.tambah_barang(Makanan("Roti Tawar", 12000, 8000, 30, "2025-06-15"))
    toko.tambah_barang(Minuman("Aqua 600ml", 5000, 3000, 50, 600))
    toko.tambah_barang(Minuman("Teh Botol", 6000, 4000, 40, 350))
    toko.tambah_barang(KebutuhanRT("Sabun Lifebuoy", 8000, 5500, 20, "Lifebuoy"))
    toko.tambah_barang(KebutuhanRT("Deterjen Rinso", 15000, 10000, 15, "Rinso"))

    # Transaksi 1
    trx1 = toko.buat_transaksi("Budi Santoso")
    trx1.tambah_item(toko.cari_barang("Indomie Goreng"), 5)
    trx1.tambah_item(toko.cari_barang("Aqua 600ml"), 2)
    trx1.selesaikan()
    print(trx1.struk())

    # Transaksi 2
    trx2 = toko.buat_transaksi("Siti Rahayu")
    trx2.tambah_item(toko.cari_barang("Sabun Lifebuoy"), 3)
    trx2.tambah_item(toko.cari_barang("Teh Botol"), 4)
    trx2.selesaikan()
    print(trx2.struk())

    # Laporan
    print()
    toko.laporan_stok()
    print()
    toko.laporan_transaksi()