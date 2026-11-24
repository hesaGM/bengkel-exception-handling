from abc import ABC, abstractmethod
# ============================================================================
# SISTEM MANAJEMEN BENGKEL - DENGAN EXCEPTION HANDLING
# ============================================================================
# Proyek UTS yang telah ditambahkan penanganan pengecualian (exception handling)
#
# KOMPONEN YANG DITAMBAHKAN:
#   1. Identifikasi 4 aturan bisnis yang dapat dilanggar
#   2. Hierarki custom exception (1 base + 3 turunan)
#   3. Setter & method menggunakan raise untuk validasi
#   4. Program utama dengan try, except, else, finally
#   5. Class diagram di README.md
# ============================================================================


# ============================================================================
# BAGIAN 1: HIERARKI CUSTOM EXCEPTION
# ============================================================================
#
# Hierarki:
#   Exception (bawaan Python)
#       └── BengkelException (base exception kustom)
#               ├── DataTidakValidError
#               ├── BisnisRuleError
#               └── LayananError
# ============================================================================

# Perubahan Kode Untuk bagian Class
class BengkelException(Exception):
    """Base exception untuk seluruh sistem bengkel."""
    def __init__(self, pesan="Terjadi kesalahan pada sistem bengkel", prefix=""):
        self.pesan = f"{prefix} {pesan}".strip()
        super().__init__(self.pesan)


class DataTidakValidError(BengkelException):
    """Error jika data input tidak valid."""
    def __init__(self, field_name, pesan):
        self.field_name = field_name
        super().__init__(f"{field_name}: {pesan}", "[Data Tidak Valid]")


class BisnisRuleError(BengkelException):
    """Error jika melanggar aturan bisnis."""
    def __init__(self, rule, pesan):
        self.rule = rule
        super().__init__(f"{rule}: {pesan}", "[Aturan Bisnis Dilanggar]")


class LayananError(BengkelException):
    """Error terkait layanan bengkel."""
    def __init__(self, pesan):
        super().__init__(pesan, "[Error Layanan]")

# class BengkelException(Exception):
    """
    BASE EXCEPTION untuk seluruh sistem bengkel.
    Semua exception kustom mewarisi dari kelas ini.
    """
    def __init__(self, pesan="Terjadi kesalahan pada sistem bengkel"):
        self.pesan = pesan
        super().__init__(self.pesan)
#
#
#class DataTidakValidError(BengkelException):
#    """Exception untuk DATA INPUT yang tidak valid."""
#    def __init__(self, field_name, pesan):
#        self.field_name = field_name
#        super().__init__(f"[Data Tidak Valid] {field_name}: {pesan}")
#
#
#class BisnisRuleError(BengkelException):
#    """Exception untuk PELANGGARAN ATURAN BISNIS."""
#    def __init__(self, rule, pesan):
#        self.rule = rule
#        super().__init__(f"[Aturan Bisnis Dilanggar] {rule}: {pesan}")
#
#
#class LayananError(BengkelException):
#    """Exception untuk kesalahan terkait LAYANAN."""
#    def __init__(self, pesan):
#        super().__init__(f"[Error Layanan] {pesan}")
#

# ============================================================================
# BAGIAN 2: ATURAN BISNIS YANG DIIDENTIFIKASI
# ============================================================================
# 4 Aturan bisnis yang dapat dilanggar:
#
# ATURAN 1: Nama pelanggan tidak boleh kosong
# ATURAN 2: Harga layanan tidak boleh negatif
# ATURAN 3: Plat nomor harus minimal 4 karakter
# ATURAN 4: Satu mekanik maksimal menangani 3 Work Order aktif
# ============================================================================


# ============================================================================
# BAGIAN 3: KELAS-KELAS DOMAIN (DENGAN EXCEPTION HANDLING DI SETTER)
# ============================================================================

class DiskonMixin:
    """Mixin untuk menghitung diskon member 10%."""
    def hitung_diskon(self, total):
        return int(total * 0.9)


class Pelanggan:
    """Kelas untuk merepresentasikan pelanggan bengkel."""
    def __init__(self, nama, is_member):
        self.nama = nama          # Memanggil setter
        self._is_member = is_member

    @property
    def nama(self):
        return self._nama

    @nama.setter
    def nama(self, nilai):
        # VALIDASI: Tipe data harus string
        if not isinstance(nilai, str):
            raise DataTidakValidError("nama", "Nama harus berupa teks (string)")
        # VALIDASI: Tidak boleh kosong (ATURAN BISNIS 1)
        if not nilai.strip():
            raise DataTidakValidError("nama", "Nama pelanggan tidak boleh kosong")
        self._nama = nilai

    def cek_member(self):
        return self._is_member


class Kendaraan(ABC):
    """
    Kelas dasar (Abstract Base Class) untuk semua jenis kendaraan.
    """
    def __init__(self, plat_nomor, merk):
        self.plat_nomor = plat_nomor
        self._merk = merk
    @property
    def plat_nomor(self):
        return self._plat_nomor
    @plat_nomor.setter
    def plat_nomor(self, nilai):
        if not isinstance(nilai, str) or len(nilai.strip()) < 4:
            raise DataTidakValidError(
                "plat_nomor",
                "Plat nomor harus minimal 4 karakter (contoh: DK 1234 AB)"
            )
        self._plat_nomor = nilai
    def info_kendaraan(self):
        return f"{self._merk} ({self._plat_nomor})"
    def __eq__(self, other):
        if isinstance(other, Kendaraan):
            return self._plat_nomor == other._plat_nomor
        return False
    @abstractmethod
    def hitung_tarif_dasar(self):
        """
        Method abstrak yang WAJIB di-override oleh subclass (Motor, Mobil).
        """
        raise NotImplementedError("Subclass Kendaraan wajib mengimplementasikan method hitung_tarif_dasar()")

class Motor(Kendaraan):
    """Kelas Motor (turunan dari Kendaraan)."""
    def __init__(self, plat_nomor, merk, jenis_motor):
        super().__init__(plat_nomor, merk)
        self._jenis_motor = jenis_motor

    def hitung_tarif_dasar(self):
        return 50000


class Mobil(Kendaraan):
    """Kelas Mobil (turunan dari Kendaraan)."""
    def __init__(self, plat_nomor, merk, tipe_mobil):
        super().__init__(plat_nomor, merk)
        self._tipe_mobil = tipe_mobil

    def hitung_tarif_dasar(self):
        return 100000


class Layanan:
    """Kelas untuk merepresentasikan layanan bengkel."""
    def __init__(self, nama_layanan, harga):
        self._nama_layanan = nama_layanan
        self.harga = harga  # Memanggil setter

    @property
    def nama_layanan(self):
        return self._nama_layanan

    @property
    def harga(self):
        return self._harga

    @harga.setter
    def harga(self, nilai):
        # VALIDASI: Harga tidak boleh negatif (ATURAN BISNIS 2)
        if not Layanan.validasi_harga(nilai):
            raise LayananError(f"Harga '{self._nama_layanan}' tidak boleh negatif (diterima: {nilai})")
        self._harga = nilai

    def get_harga(self):
        return self._harga

    @staticmethod
    def validasi_harga(harga):
        """Static method: mengecek apakah harga valid (>= 0)."""
        return isinstance(harga, (int, float)) and harga >= 0


class WorkOrder(DiskonMixin):
    """Kelas Work Order - Menggunakan Multiple Inheritance (Mixin)."""
    total_wo = 0
    _wo_per_mekanik = {}  # Tracker jumlah WO per mekanik

    def __init__(self, id_wo, pelanggan, kendaraan, mekanik):
        # VALIDASI ATURAN BISNIS 4: Mekanik maksimal 3 WO aktif
        jumlah_wo_mekanik = WorkOrder._wo_per_mekanik.get(mekanik, 0)
        if jumlah_wo_mekanik >= 3:
            raise BisnisRuleError(
                "Batas WO Mekanik",
                f"Mekanik '{mekanik}' sudah menangani {jumlah_wo_mekanik} WO (maks 3)"
            )

        self._id_wo = id_wo
        self._mekanik = mekanik
        self._status = "Antre"

        # AGGREGATION: Objek diterima dari luar
        self._pelanggan = pelanggan
        self._kendaraan = kendaraan

        # COMPOSITION: Objek Layanan dibuat DI DALAM constructor
        tarif = self._kendaraan.hitung_tarif_dasar()
        layanan_utama = Layanan("Jasa Servis Dasar", tarif)
        self._daftar_layanan = [layanan_utama]

        # Update tracker
        WorkOrder._wo_per_mekanik[mekanik] = jumlah_wo_mekanik + 1
        WorkOrder.total_wo += 1

    def tambah_layanan(self, layanan_baru):
        """Menambahkan layanan ke Work Order. Raise jika duplikat."""
        for l in self._daftar_layanan:
            if l.nama_layanan == layanan_baru.nama_layanan:
                raise LayananError(
                    f"Layanan '{layanan_baru.nama_layanan}' sudah ada di WO ini"
                )
        self._daftar_layanan.append(layanan_baru)

    def hitung_total(self):
        total = sum(l.get_harga() for l in self._daftar_layanan)
        if self._pelanggan.cek_member():
            total = self.hitung_diskon(total)
        return total

    def __str__(self):
        return f"WO: {self._id_wo} | Status: {self._status} | Mekanik: {self._mekanik}"

    @classmethod
    def reset_tracker(cls):
        """Reset tracker WO per mekanik."""
        cls._wo_per_mekanik = {}
        cls.total_wo = 0


# ============================================================================
# BAGIAN 4: PROGRAM UTAMA DENGAN TRY, EXCEPT, ELSE, FINALLY
# ============================================================================

if __name__ == "__main__":

    print("=" * 55)
    print("  SISTEM MANAJEMEN BENGKEL - EXCEPTION HANDLING")
    print("=" * 55)

    # --- SKENARIO 1: Alur Normal (Sukses) ---
    print("\n--- Skenario 1: Alur Normal (Data Valid) ---")

    try:
        pelanggan1 = Pelanggan("Budi", True)
        motor1 = Motor("DK 1234 AB", "Honda", "Bebek")
        wo1 = WorkOrder("WO-001", pelanggan1, motor1, "Andi")
        layanan_tambahan = Layanan("Ganti Kampas", 30000)
        wo1.tambah_layanan(layanan_tambahan)

    except BengkelException as e:
        print(f"  Error: {e}")

    else:
        print(f"  {wo1}")
        print(f"  Pelanggan : {pelanggan1.nama} (Member)")
        print(f"  Kendaraan : {motor1.info_kendaraan()}")
        print(f"  Total     : Rp {wo1.hitung_total():,}")

    finally:
        print("  [finally] Skenario 1 selesai.")

    # --- SKENARIO 2: Nama Pelanggan Kosong ---
    print("\n--- Skenario 2: Nama Pelanggan Kosong ---")

    try:
        pelanggan_error = Pelanggan("", False)

    except DataTidakValidError as e:
        print(f"  Error: {e}")

    finally:
        print("  [finally] Skenario 2 selesai.")

    # --- SKENARIO 3: Harga Layanan Negatif ---
    print("\n--- Skenario 3: Harga Layanan Negatif ---")

    try:
        layanan_error = Layanan("Ganti Oli", -5000)

    except LayananError as e:
        print(f"  Error: {e}")

    finally:
        print("  [finally] Skenario 3 selesai.")

    # --- SKENARIO 4: Plat Nomor Tidak Valid ---
    print("\n--- Skenario 4: Plat Nomor Tidak Valid ---")

    try:
        motor_error = Motor("AB", "Suzuki", "Sport")

    except DataTidakValidError as e:
        print(f"  Error: {e}")

    finally:
        print("  [finally] Skenario 4 selesai.")

    # --- SKENARIO 5: Mekanik Melebihi Batas 3 WO ---
    print("\n--- Skenario 5: Mekanik Melebihi Batas 3 WO ---")

    try:
        p = Pelanggan("Customer", False)
        m = Motor("DK 5555 XX", "Yamaha", "Matic")

        wo_a = WorkOrder("WO-A", p, m, "Dewa")
        wo_b = WorkOrder("WO-B", p, m, "Dewa")
        wo_c = WorkOrder("WO-C", p, m, "Dewa")
        print("  WO-A, WO-B, WO-C berhasil dibuat untuk mekanik Dewa")

        # WO ke-4 -> melebihi batas
        wo_d = WorkOrder("WO-D", p, m, "Dewa")

    except BisnisRuleError as e:
        print(f"  Error: {e}")

    finally:
        print("  [finally] Skenario 5 selesai.")

    # --- SKENARIO 6: Layanan Duplikat ---
    print("\n--- Skenario 6: Layanan Duplikat ---")

    try:
        pelanggan2 = Pelanggan("Sari", False)
        mobil1 = Mobil("DK 9999 CD", "Toyota", "SUV")
        wo2 = WorkOrder("WO-002", pelanggan2, mobil1, "Rio")

        wo2.tambah_layanan(Layanan("Ganti Oli", 50000))
        print("  Layanan 'Ganti Oli' berhasil ditambahkan")

        # Tambah layanan duplikat
        wo2.tambah_layanan(Layanan("Ganti Oli", 50000))

    except LayananError as e:
        print(f"  Error: {e}")

    else:
        print("  Semua layanan berhasil ditambahkan")

    finally:
        print("  [finally] Skenario 6 selesai.")

    # --- SKENARIO 7: Tangkap Semua dengan Base Exception ---
    print("\n--- Skenario 7: Tangkap dengan Base Exception ---")

    try:
        pelanggan_x = Pelanggan(123, True)  # Nama bukan string

    except BengkelException as e:
        print(f"  Error: {e}")
        print(f"  Tipe : {type(e).__name__}")

    finally:
        print("  [finally] Skenario 7 selesai.")

    # --- SKENARIO 8: Perbandingan Kendaraan ---
    print("\n--- Skenario 8: Perbandingan Kendaraan (__eq__) ---")

    try:
        motor_a = Motor("DK 1234 AB", "Honda", "Bebek")
        motor_b = Motor("DK 1234 AB", "Yamaha", "Matic")
        motor_c = Motor("DK 5678 CD", "Suzuki", "Sport")

    except DataTidakValidError as e:
        print(f"  Error: {e}")

    else:
        print(f"  motor_a == motor_b? {motor_a == motor_b}")   # True
        print(f"  motor_a == motor_c? {motor_a == motor_c}")   # False

    finally:
        print("  [finally] Skenario 8 selesai.")

    print("\n" + "=" * 55)
    print("  Semua skenario selesai.")
    print("=" * 55)
