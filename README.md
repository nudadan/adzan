# Adzan Scheduler

Script `update_adzan_schedule.py` digunakan untuk mengambil jadwal sholat harian kota Bandung dari API Aladhan dan membuat cron job untuk memutar file MP3 adzan secara otomatis.

## Persiapan

- Python 3
- Module `requests` dan `python-crontab`
- Pemutar MP3 `mpg123`
- File `adzan_subuh.mp3` dan `adzan_umum.mp3` berada di direktori yang sama dengan script

Install dependensi Python menggunakan pip:

```bash
pip install requests python-crontab
```

## Menjalankan

Jalankan script setiap hari (misalnya melalui cron atau systemd):

```bash
python3 update_adzan_schedule.py
```

Script akan:

1. Mengambil jadwal sholat hari ini.
2. Menyimpan jadwal ke `jadwal_sholat.json`.
3. Memperbarui cron job dengan komentar `adzan_schedule` untuk memutar adzan pada waktunya.

Pesan sukses akan ditampilkan setelah cron job diperbarui.
