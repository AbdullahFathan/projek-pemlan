import csv
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
from services import FireServices

LOGO = "E:/Hal UB/Semester 5/Pemlan/sistem antri klinik/klinik/LOGO.png"

# DATA PROCESS ANTRIAN
class DataAntrian:
    def __init__(self):
        self.pasien_list = []       # LIST UNTUK DITAMPILKAN DI LISTBOX
        self.rekap_pasien = []      # LIST UNTUK DISIMPAN KE CSV

    # TAMBAH PASIEN
    def add_pasien(self, nama):
        if nama:
            if self.rekap_pasien:
                nomor_antrian_terakhir = self.rekap_pasien[-1][0]
                nomor_antrian = nomor_antrian_terakhir + 1
            else:
                nomor_antrian = 1
            self.pasien_list.append((nomor_antrian, nama))
            self.rekap_pasien.append((nomor_antrian, nama))
            return nomor_antrian
        return None

    # NEXT PASIEN
    def next_pasien(self):
        if self.pasien_list:
            nomor_antrian, nama = self.pasien_list.pop(0)
            FireServices.next_pasien()
            return nomor_antrian, nama
        return None

    # MENAMPILKAN LIST PASIEN
    def list_pasien(self):
        return self.pasien_list

    # SAVE REKAP DATA KE CSV
    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Nomor Antrian', 'Nama Pasien']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for nomor_antrian, nama in self.rekap_pasien:
                if nomor_antrian >= 1:
                    writer.writerow({'Nomor Antrian': nomor_antrian, 'Nama Pasien': nama})

# TAMPILAN APLIKASI
class AppKlinik:
    # INISIALISASI & BACKGROUND
    def __init__(self, window):
        self.window = window
        self.window.title("Aplikasi Antrian Klinik X")
        self.window.iconphoto(False, ImageTk.PhotoImage(Image.open(LOGO)))
        self.window.configure(bg="#f2e8cf")
        self.window.attributes("-fullscreen", True)

        self.DataAntrian = DataAntrian()

        self.interface()

    # TAMPILAN UTAMA
    def interface(self):
        self.header()
        self.add_next_pasien()
        self.list_pasien()

    # TAMPILAN HEADER
    def header(self):
        frame_header = tk.Frame(
            self.window,
            background="#386641"
        )
        frame_header.pack(side="top", fill="x")

        # TAMPILAN LOGO
        image = Image.open(LOGO)
        resized_image = image.resize((150, 150), Image.ANTIALIAS)
        fixed_logo = ImageTk.PhotoImage(resized_image)
        logo = tk.Label(
            frame_header,
            image=fixed_logo,
            background="#386641"
        )
        logo.image = fixed_logo
        logo.pack(side="left", padx=10, pady=10)

        # NAMA APLIKASI
        app_label = tk.Label(
            frame_header,
            text="Antrian Klinik X",
            font=("Arial", 32),
            fg="white",
            background="#386641"
        )
        app_label.pack(side="left", padx=20)

        # TOMBOL EXIT
        exit_button = tk.Button(
            frame_header,
            text="X",
            command=self.save_csv,
            font=("Arial", 16),
            fg="white",
            background="dark red"
        )
        exit_button.pack(side="right", padx=20)

    # FUNGSI EXIT DAN SAVE KE CSV
    def save_csv(self):
        file_name = 'rekap_antrian.csv'
        self.DataAntrian.save_to_csv(file_name)
        FireServices.delete_all_pasien()
        self.window.quit()

    # TAMPILAN TAMBAH DAN NEXT PASIEN
    def add_next_pasien(self):
        frame_add_next_pasien = tk.Frame(
            self.window,
            background="#f2e8cf"
        )
        frame_add_next_pasien.pack(side="left", fill="both", padx=10, pady=20, expand=True)

        # BAGIAN TAMBAH PASIEN
        tambah_pasien_label = tk.Label(
            frame_add_next_pasien,
            text="Nama Pasien",
            font=("Arial", 20),
            fg="#386641",
            background="#f2e8cf"
        )
        tambah_pasien_label.pack(anchor="n", padx=10, pady=10)

        tambah_pasien = tk.Entry(
            frame_add_next_pasien,
            font=("Arial", 16)
        )
        tambah_pasien.pack(fill="both", padx=10, pady=10)
        tambah_pasien.bind("<Return>", lambda event: submit_nama())
        
        # BAGIAN SUBMIT NAMA PASIEN
        def submit_nama():
            name = tambah_pasien.get()

            nomor_antrian = self.DataAntrian.add_pasien(name)
            id = FireServices.add_pasien(name, nomor_antrian)

            #* ini pop up tampilin 
            messagebox.showinfo("Informasi", f"Pasien {name} (Nomor Antrian: {nomor_antrian}) (ID: {id}).")
            if nomor_antrian is not None:
                tambah_pasien.delete(0, tk.END)
                self.update_listbox()

        submit_button = tk.Button(
            frame_add_next_pasien,
            text="Submit",
            font=("Arial", 18),
            command=submit_nama,
            bg="#386641",
            fg="white",
            relief=tk.FLAT
        )
        submit_button.pack(pady=10)

        # BAGIAN TOMBOL NEXT
        def button_next():
            next_patient = self.DataAntrian.next_pasien()

            if next_patient:
                queue_number, name = next_patient
                messagebox.showinfo("Informasi", f"Pasien selanjutnya adalah {name} (Nomor Antrian {queue_number}).")
            else:
                messagebox.showinfo("Informasi", "Tidak ada pasien yang terdaftar di antrian.")

            self.update_listbox()

        next_button = tk.Button(
            frame_add_next_pasien,
            text="Pasien Selanjutnya",
            font=("Arial", 18),
            command=button_next,
            bg="#386641",
            fg="white",
            relief=tk.FLAT
        )
        next_button.pack(pady=100)

    # BOX MENAMPILKAN LIST PASIEN
    def list_pasien(self):
        frame_listPasien = tk.Frame(
            self.window,
            background="#f2e8cf"
        )
        frame_listPasien.pack(side="right", fill="both", padx=10, pady=20)

        list_label = tk.Label(
            frame_listPasien,
            text="List Antrian Pasien",
            font=("Arial", 24),
            fg="#386641",
            background="#f2e8cf"
        )
        list_label.pack(fill="both")

        listbox = tk.Listbox(
            frame_listPasien,
            width=120,
            font=("Arial", 14),
            relief=tk.FLAT
        )
        listbox.pack(padx=10, pady=10, fill="both", expand=True)

        self.listbox = listbox
        self.update_listbox()

    # FUNGSI MENGUPDATE ISI LISTBOX OTOMATIS
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for nomor_antrian, nama in self.DataAntrian.list_pasien():
            self.listbox.insert(tk.END, f"{nomor_antrian}. {nama}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppKlinik(root)
    root.mainloop()