#!/usr/bin/env python3
"""

TEMPLATE TP4 DDP1 Semester Gasal 2019/2020

Author: 
Ika Alfina (ika.alfina@cs.ui.ac.id)
Evi Yulianti (evi.yulianti@cs.ui.ac.id)
Meganingrum Arista Jiwanggi (meganingrum@2cs.ui.ac.id)

Last update: 23 November 2019

Modification:
Dennis Al Baihaqi Walangadi (dennis.al@ui.ac.id) (1906400141)

Last edit: 7 December 2019

"""
import os
from budayaKB_model import *
from flask import Flask, request, render_template, Response

app = Flask(__name__)
app.secret_key = "tp4"

# inisialisasi objek budayaData
budayaData = BudayaCollection()

# variabel flask yang akan digunakan
UPLOAD_FOLDER = os.path.join(os.getcwd())
ALLOWED_EXTENSIONS = {'csv', 'txt'}

def file_check(file):
    return '.' in file and file.rsplit('.', 1)[-1] in ALLOWED_EXTENSIONS

# merender tampilan default(index.html)
@app.route('/')
def index():
    return render_template("index.html")


# Bagian ini adalah implementasi fitur Impor dan Ekspor Budaya, yaitu:
# - merender tampilan saat menu Impor/Ekspor diklik
# - melakukan pemrosesan terhadap isian form setelah tombol "Unggah" atau "Unduh" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport
# - memberikan file berupa data di dalam database kepada user
@app.route('/impor', methods=['GET', 'POST'])
def import_ekspor():
    if request.method == "GET":
        return render_template("impor.html")

    elif request.method == "POST" and 'imporcsv' in request.files:

        f = request.files['imporcsv']
        if file_check(f.filename):
            savepath = os.path.join(UPLOAD_FOLDER, f.filename)  # Cari path file yang ingin kita ambil
            f.save(savepath)  # Simpan file yang dituju ke dalam root folder
            databasefilename = f.filename  # Ambil nama file
            count = budayaData.importFromCSV(savepath)  # Impor dan hitung berapa line yang kita input
            os.remove(savepath)  # Hapus file sementara yang telah kita upload
            if count > 0:
                return render_template("impor.html", count=count, filename=databasefilename, impor=1)
            else:
                return render_template("impor.html", impor=0)
        else:
            return render_template("impor.html", impor=0)

    elif request.method == "POST":
        flag = budayaData.exportToCSV("exported.csv")  # Ekspor data ke dalam file bernama exported.csv

        if flag == 1:  # Jika ekspor berhasil
            with open("exported.csv") as fp:  # Buka file hasil ekspor
                csvread = fp.read()  # Baca seluruh file tersebut
                return Response(  # Berikan seluruh file yang telah dibaca ke sebuah file CSV
                    csvread,
                    mimetype="text/csv",
                    headers={"Content-disposition": "attachment; filename=BudayaKB-Lite.csv"})

        else:  # Kalau gagal, beri peringatan
            return render_template("impor.html", ekspor=0)


# Bagian ini adalah implementasi fitur Tambah Budaya, yaitu:
# - merender tampilan saat menu Tambah diklik
# - melakukan pemrosesan terhadap isian form setelah tombol "Tambah" diklik
# - menampilkan notifikasi bahwa data telah berhasil ditambahkan
@app.route('/tambah', methods=['GET', 'POST'])
def tambah_data():
    if request.method == 'GET':
        return render_template("tambah.html", data=budayaData.koleksi)  # Berikan tabel data untuk acuan user

    elif request.method == "POST":
        datainput = request.form  # Mengambil data dan membuat kedalam dictionary
        # Menambahkan data
        success = budayaData.tambah(datainput['Nama'], datainput['Tipe'], datainput['Provinsi'], datainput['Referensi'])
        # Beri tahu user kalau data berhasil ditambahkan
        return render_template("tambah.html", result=datainput['Nama'], data=budayaData.koleksi, success=success)


# Bagian ini adalah implementasi fitur Ubah Budaya, yaitu:
# - merender tampilan saat menu Ubah diklik
# - melakukan pemrosesan terhadap isian form setelah tombol "Update" diklik
# - menampilkan notifikasi bahwa data telah berhasil diubah
@app.route('/ubah', methods=['GET', 'POST'])
def ubah_data():
    if request.method == 'GET':
        keys = sorted(budayaData.koleksi.keys())
        # Beri user pilihan data apa saja yang ingin ubah
        return render_template("ubah.html", data=budayaData.koleksi, keys=keys)

    elif request.method == 'POST':
        datainput = request.form
        # Ubah data yang ingin dipilih, karena data sudah kita sediakan, tidak akan ada exception
        success = budayaData.ubah(datainput['Nama'], datainput['Tipe'], datainput['Provinsi'], datainput['Referensi'])
        # Beritahu user kalau data sudah kita ubah
        return render_template("ubah.html", terubah=datainput['Nama'], result=success, data=budayaData.koleksi)


# Bagian ini adalah implementasi fitur Hapus Budaya, yaitu:
# - merender tampilan saat menu Hapus diklik
# - melakukan pemrosesan terhadap isian form setelah tombol "Hapus" atau "Haus database" diklik
# - menampilkan notifikasi bahwa data telah berhasil dihapus
@app.route('/hapus', methods=['GET', 'POST'])
def hapus_data():
    if request.method == 'GET':
        keys = sorted(budayaData.koleksi.keys())
        # Beri user pilihan data apa saja yang ingin hapus
        return render_template("hapus.html", data=budayaData.koleksi, keys=keys)

    elif request.method == 'POST' and "Nama" in request.form:
        datainput = request.form  # Ambil formulir user
        deletion = budayaData.hapus(datainput['Nama'])  # Hapus berdasarkan nama data yang dipilih
        keys = sorted(budayaData.koleksi.keys())  # Update pilihan data
        return render_template("hapus.html", result=deletion, terhapus=datainput['Nama'], data=budayaData.koleksi,
                               keys=keys)

    elif request.method == 'POST':
        # tidak terdapat formulir dalam POST, maka user meminta untuk seluruh database dihapus
        budayaData.koleksi.clear()  # Hapus seluruh data di dalam database
        return render_template("hapus.html", result=1, terhapus="Seluruh data", data=budayaData.koleksi)


# Bagian ini adalah implementasi fitur Cari Budaya, yaitu:
# - merender tampilan saat menu Cari diklik
# - melakukan pemrosesan terhadap isian form setelah tombol "Cari" diklik
# - menampilkan data secara real-time
@app.route('/cari', methods=['GET', 'POST'])
def cari_data():
    if request.method == 'GET':
        return render_template("cari.html", kumpulbudaya=budayaData.koleksi)

    elif request.method == 'POST':
        tipe = request.form['Tipe']  # Ambil formulir Tipe dari user
        teks = request.form['Teks']  # Ambil formulir Teks dari user

        # Cek tipe yang ingin kita cari
        if tipe == 'Nama':
            result = budayaData.cariByNama(teks)
            return render_template("cari.html", result=result, kumpulbudaya=budayaData.koleksi)
        elif tipe == 'Tipe':
            result = budayaData.cariByTipe(teks)
            return render_template("cari.html", result=result, kumpulbudaya=budayaData.koleksi)

        elif tipe == 'Provinsi':
            result = budayaData.cariByProv(teks)
            return render_template("cari.html", result=result, kumpulbudaya=budayaData.koleksi)

        # Kalau tidak ada, beri tampilan default
        else:
            return render_template("cari.html", kumpulbudaya=budayaData.koleksi)


# Bagian ini adalah implementasi fitur Statistik Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik
# - melakukan visualisasi data menggunakan Chart.js
# - menampilkan tabel data berdasarkan tipe dan provinsi budaya
@app.route('/statistik', methods=['GET', 'POST'])
def stat_data():
    # PERSIAPAN DATA
    # Stat Prov
    provsorteddata = sorted(budayaData.statByProv().items(), key=lambda x: x[1], reverse=True)
    provlistofkey = [x[0] for x in provsorteddata]  # Pasti paralel
    provlistofvalue = [x[1] for x in provsorteddata]
    provnums = len(provlistofkey)  # Banyaknya provinsi yang berbeda di dalam database

    # Stat Tipe
    tipesorteddata = sorted(budayaData.statByTipe().items(), key=lambda x: x[1], reverse=True)
    tipelistofkey = [x[0] for x in tipesorteddata]  # Pasti paralel
    tipelistofvalue = [x[1] for x in tipesorteddata]
    tipenums = len(tipelistofkey)  # Banyaknya tipe budaya yang berbeda di dalam database

    # Stat
    stat = budayaData.stat()
    if request.method == 'GET':
        # Penyajian data
        return render_template("stat.html", databudaya=budayaData.koleksi, provlabel=provlistofkey,
                               provdata=provlistofvalue, provnums=provnums,
                               provraw=provsorteddata, tipelabel=tipelistofkey,
                               tipedata=tipelistofvalue, tipenums=tipenums,
                               tiperaw=tipesorteddata, stat=stat)


# run main app
if __name__ == "__main__":
    app.run()
    # app.run(debug=True)
