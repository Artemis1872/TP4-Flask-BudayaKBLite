#!/usr/bin/env python3
"""

TEMPLATE TP4 DDP1 Semester Gasal 2019/2020

Author: 
Ika Alfina (ika.alfina@cs.ui.ac.id)
Evi Yulianti (evi.yulianti@cs.ui.ac.id)
Meganingrum Arista Jiwanggi (meganingrum@2cs.ui.ac.id)

Last update: 23 November 2019

"""
from budayaKB_model import *
from flask import Flask, request, render_template, redirect, flash
from wtforms import Form, validators, TextField

app = Flask(__name__)
app.secret_key = "tp4"

# inisialisasi objek budayaData
# databasefilename = ""
budayaData = BudayaCollection()


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

	elif request.method == "POST":
		f = request.files['file']

		print(f)
		databasefilename = f.filename
		print(databasefilename)
		result_impor = budayaData.importFromCSV(f.filename)
		
		# budayaData.exportToCSV(databasefilename)  # setiap perubahan data langsung disimpan ke file
		return render_template("impor.html", result=result_impor, fname=f.filename)


@app.route('/tambahBudaya', methods=['GET', 'POST'])
def tambahData():
	if request.method == 'GET':
		return render_template("tambahBudaya.html")

	elif request.method == "POST":
		datainput = request.form  # Mengambil data dan membuat kedalam dictionary
		budayaData.tambah(datainput['Nama'], datainput['Tipe'], datainput['Provinsi'], datainput['Referensi'])
		print(budayaData)
		return render_template("tambahBudaya.html", result=datainput['Nama'], data=datainput)

@app.route('/ubah', methods=['GET', 'POST'])
def ubahData():
	if request.method == 'GET':
		return render_template("ubah.html")

	elif request.method == 'POST':
		datainput = request.form
		success = budayaData.ubah(datainput['Nama'], datainput['Tipe'], datainput['Provinsi'], datainput['Referensi'])
		print(budayaData)
		return render_template("ubah.html", result=success, data=datainput)


@app.route('/hapusBudaya', methods=['GET', 'POST'])
def hapusData():
	if request.method == 'GET':
		return render_template("hapusbudaya.html")

	elif request.method == 'POST':
		datainput = request.form
		deletion = budayaData.hapus(datainput['Nama'])
		print(budayaData)
		return render_template("hapusbudaya.html", result=deletion, budaya=datainput['Nama'])

@app.route('/cari', methods=['GET', 'POST'])
def cariData():
	if request.method == 'GET':
		return render_template("cari.html")

	elif request.method == 'POST':
		datainput = request.form
		data = None
		print(datainput['Nama'])
		print(datainput['Tipe'])
		print(datainput['Provinsi'])
		# if datainput['Nama'] != '':
		# 	data = budayaData.cariByNama(datainput['Nama'])
		# elif datainput['Tipe'] != '':
		# 	data = budayaData.cariByTipe(datainput['Tipe'])
		# elif datainput['Provinsi'] != '':
		# 	data = budayaData.cariByProv(datainput['Provinsi'])
		# else:
		return render_template("cari.html")
	return render_template("cari.html")

@app.route('/statsBudaya', methods=['GET', 'POST'])
def statData():
	if request.method == 'GET':
		banyak = budayaData.stat()
		return render_template("statistik.html", count=banyak)

	elif request.method == 'POST':
		return render_template("statistik.html")


# run main app
if __name__ == "__main__":
	app.run(debug=True)
