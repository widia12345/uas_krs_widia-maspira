import tkinter as tk
from tkinter import messagebox
import sqlite3

# Aplikasi KRS Mahasiswa
# Dibuat untuk input dan kelola data KRS mahasiswa.
# Pake GUI Tkinter dan database lokal SQLite
# Mata kuliah dan SKS sesuai semester, histori tetap disimpan meski data dinonaktifkan.

# Koneksi ke database lokal
conn = sqlite3.connect('krs.db')
cursor = conn.cursor()

# Buat tabel jika belum ada
cursor.execute('''
    CREATE TABLE IF NOT EXISTS krs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        nim TEXT,
        angkatan TEXT,
        jurusan TEXT,
        fakultas TEXT,
        matkul TEXT,
        sks INTEGER,
        aktif INTEGER DEFAULT 1,
        waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# Fungsi simpan data ke database

def simpan_data():
    nama = ent_nama.get()
    nim = ent_nim.get()
    angkatan = ent_angkatan.get()
    jurusan = ent_jurusan.get()
    fakultas = ent_fakultas.get()

    matkul_terpilih = []
    total_sks = 0
    for mk, sks, var in daftar_mk:
        if var.get():
            matkul_terpilih.append(f"{mk} ({sks} SKS)")
            total_sks += sks

    gabungan_mk = ", ".join(matkul_terpilih)

    try:
        cursor.execute("INSERT INTO krs (nama, nim, angkatan, jurusan, fakultas, matkul, sks, aktif) VALUES (?, ?, ?, ?, ?, ?, ?, 1)",
                       (nama, nim, angkatan, jurusan, fakultas, gabungan_mk, total_sks))
        conn.commit()
        messagebox.showinfo("Berhasil", "Data KRS berhasil disimpan.")
    except Exception as err:
        messagebox.showerror("Gagal", f"Terjadi kesalahan: {err}")

# Soft delete berdasarkan NIM

def hapus_semua():
    nim = ent_nim.get()
    try:
        cursor.execute("UPDATE krs SET aktif = 0 WHERE nim = ?", (nim,))
        conn.commit()
        messagebox.showinfo("OK", "Semua data KRS untuk NIM tersebut dinonaktifkan.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Pulihkan semua data berdasarkan NIM

def pulihkan_semua():
    nim = ent_nim.get()
    try:
        cursor.execute("UPDATE krs SET aktif = 1 WHERE nim = ?", (nim,))
        conn.commit()
        messagebox.showinfo("OK", "Semua data KRS untuk NIM tersebut telah dipulihkan.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Hapus 1 data berdasarkan ID

def hapus_per_id():
    id_target = ent_idhapus.get()
    try:
        cursor.execute("UPDATE krs SET aktif = 0 WHERE id = ?", (id_target,))
        conn.commit()
        messagebox.showinfo("OK", f"Data ID {id_target} dinonaktifkan.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tampilkan semua histori data

def tampilkan_histori():
    win = tk.Toplevel()
    win.title("Histori KRS")
    hasil = cursor.execute("SELECT id, nama, nim, matkul, sks, aktif, waktu FROM krs ORDER BY waktu DESC").fetchall()
    for idx, row in enumerate(hasil):
        status = "AKTIF" if row[5] else "NONAKTIF"
        teks = f"ID: {row[0]} | {row[1]} ({row[2]}) | {row[3]} | SKS: {row[4]} | {status} | {row[6]}"
        tk.Label(win, text=teks, anchor="w").pack(fill="x")

# GUI Utama
root = tk.Tk()
root.title("Aplikasi KRS Mahasiswa")

# Input data mahasiswa
tk.Label(root, text="Nama").grid(row=0, column=0)
ent_nama = tk.Entry(root)
ent_nama.grid(row=0, column=1)

tk.Label(root, text="NIM").grid(row=1, column=0)
ent_nim = tk.Entry(root)
ent_nim.grid(row=1, column=1)

tk.Label(root, text="Angkatan").grid(row=2, column=0)
ent_angkatan = tk.Entry(root)
ent_angkatan.grid(row=2, column=1)

tk.Label(root, text="Jurusan").grid(row=3, column=0)
ent_jurusan = tk.Entry(root)
ent_jurusan.grid(row=3, column=1)

tk.Label(root, text="Fakultas").grid(row=4, column=0)
ent_fakultas = tk.Entry(root)
ent_fakultas.grid(row=4, column=1)

# Mata kuliah
tk.Label(root, text="Pilih Mata Kuliah").grid(row=5, column=0, sticky="nw")
daftar_mk = [
    ("Artificial Intelligence", 2, tk.IntVar()),
    ("Praktik Artificial Intelligence", 1, tk.IntVar()),
    ("Smart City", 2, tk.IntVar()),
    ("Interaksi Manusia Komputer", 2, tk.IntVar()),
    ("Web Framework (Full stack Development)", 2, tk.IntVar()),
    ("Praktik Web Framework (Full stack Development)", 2, tk.IntVar()),
    ("Cybersecurity", 2, tk.IntVar()),
    ("Pemrograman Berorientasi Objek", 2, tk.IntVar()),
    ("Praktik Pemrograman Berorientasi Objek", 2, tk.IntVar()),
]
for idx, (mk, sks, var) in enumerate(daftar_mk):
    tk.Checkbutton(root, text=f"{mk} ({sks} SKS)", variable=var).grid(row=5+idx, column=1, sticky="w")

# Tombol aksi
tk.Button(root, text="Simpan", command=simpan_data).grid(row=15, column=0, pady=5)
tk.Button(root, text="Hapus Semua (NIM)", command=hapus_semua).grid(row=15, column=1, pady=5)
tk.Button(root, text="Pulihkan Semua (NIM)", command=pulihkan_semua).grid(row=16, column=1, pady=5)
tk.Button(root, text="Lihat Histori", command=tampilkan_histori).grid(row=16, column=0, pady=5)

# Hapus berdasarkan ID
tk.Label(root, text="ID yang ingin dihapus:").grid(row=17, column=0)
ent_idhapus = tk.Entry(root)
ent_idhapus.grid(row=17, column=1)
tk.Button(root, text="Hapus Berdasarkan ID", command=hapus_per_id).grid(row=18, column=1)

root.mainloop()
