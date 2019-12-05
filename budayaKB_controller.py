#!/usr/bin/env python3
"""

TEMPLATE TP4 DDP1 Semester Gasal 2019/2020

Author: 
Ika Alfina (ika.alfina@cs.ui.ac.id)
Evi Yulianti (evi.yulianti@cs.ui.ac.id)
Meganingrum Arista Jiwanggi (meganingrum@2cs.ui.ac.id)

Last update: 23 November 2019

"""
import os
from budayaKB_model import *
from flask import Flask, request, render_template, redirect, flash, Response
from wtforms import Form, validators, TextField

app = Flask(__name__)
app.secret_key = "tp4"

# inisialisasi objek budayaData
# databasefilename = ""
budayaData = BudayaCollection()
UPLOAD_FOLDER = os.path.join(os.getcwd())
ALLOWED_EXTENSIONS = {'csv', 'txt'}


# merender tampilan default(index.html)
@app.route('/')
def index():
	return render_template("index.html")


# Bagian ini adalah implementasi fitur Impor Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Import Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport 	
@app.route('/impor', methods=['GET', 'POST'])
def importData():
	if request.method == "GET":
		return render_template("impor.html")

	elif request.method == "POST" and 'imporcsv' in request.files:

		f = request.files['imporcsv']
		savepath = os.path.join(UPLOAD_FOLDER, f.filename)

		f.save(savepath)
		databasefilename = f.filename
		count = budayaData.importFromCSV(savepath)
		os.remove(savepath)
		#budayaData.exportToCSV("exported.csv")  # setiap perubahan data langsung disimpan ke file
		if count > 0:
			return render_template("impor.html", count=count, filename=databasefilename, impor=1)
		else:
			return render_template("impor.html", impor=0)

	elif request.method == "POST":
		flag = budayaData.exportToCSV("exported.csv")

		if flag == 1:
			with open("exported.csv") as fp:
				csv = fp.read()
				return Response(
					csv,
					mimetype="text/csv",
					headers={"Content-disposition": "attachment; filename=BudayaKB-Lite.csv"})
		else:
			return render_template("impor.html", ekspor=0)


@app.route('/tambah', methods=['GET', 'POST'])
def tambahData():
	if request.method == 'GET':
		return render_template("tambah.html", data=budayaData.koleksi)

	elif request.method == "POST":
		datainput = request.form  # Mengambil data dan membuat kedalam dictionary
		success = budayaData.tambah(datainput['Nama'], datainput['Tipe'], datainput['Provinsi'], datainput['Referensi'])
		return render_template("tambah.html", result=datainput['Nama'], data=budayaData.koleksi, success=success)


@app.route('/ubah', methods=['GET', 'POST'])
def ubahData():
	if request.method == 'GET':
		return render_template("ubah.html", data=budayaData.koleksi)

	elif request.method == 'POST':
		datainput = request.form
		success = budayaData.ubah(datainput['Nama'], datainput['Tipe'], datainput['Provinsi'], datainput['Referensi'])
		return render_template("ubah.html", terubah=datainput['Nama'], result=success, data=budayaData.koleksi)


@app.route('/hapus', methods=['GET', 'POST'])
def hapusData():
	if request.method == 'GET':
		return render_template("hapus.html", data=budayaData.koleksi)

	elif request.method == 'POST':
		datainput = request.form
		deletion = budayaData.hapus(datainput['Nama'])
		return render_template("hapus.html", result=deletion, terhapus=datainput['Nama'], data=budayaData.koleksi)


@app.route('/cari', methods=['GET', 'POST'])
def cariData():
	if request.method == 'GET':
		return render_template("cari.html", kumpulbudaya=budayaData.koleksi)

	elif request.method == 'POST':
		tipe = request.form['Tipe']
		teks = request.form['Teks']
		print(tipe)
		print(teks)

		if tipe == 'Nama':
			result = budayaData.cariByNama(teks)
			return render_template("cari.html", result=result)
		elif tipe == 'Tipe':
			result = budayaData.cariByTipe(teks)
			return render_template("cari.html", result=result)

		elif tipe == 'Provinsi':
			result = budayaData.cariByProv(teks)
			return render_template("cari.html", result=result)
		else:
			return render_template("cari.html", kumpulbudaya=budayaData.koleksi)


@app.route('/statistik', methods=['GET', 'POST'])
def statData():
	if request.method == 'GET':
		banyak = budayaData.stat()
		return render_template("stat.html")

	elif request.method == 'POST':
		return render_template("stat.html")


# run main app
if __name__ == "__main__":
	app.run(debug=True)
