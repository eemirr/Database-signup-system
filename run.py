
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys,csv,time
import sqlite3 as sql



class Main(QTabWidget):

	"""

	Basit Veritabanı Yönetim Arayüzü

	basic database management interface
	"""

	def __init__(self):
		super(Main, self).__init__()


		self.dbname = 'data.db'
		self.tablename = 'kayıt'

		self.con = sql.Connection(self.dbname)
		self.csr = self.con.cursor()
		self.csr.execute('CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY,title TEXT,side TEXT,data1 TEXT,data2 TEXT)'.format(self.tablename))
		self.con.commit()
		self.run()

	def run(self):
		self.setGeometry(315,75,675,645)
		self.tablo1 = QWidget()
		self.tablo2 = QWidget()
		self.tablo3 = QWidget()
		self.tablo4 = QWidget()

		self.kayıt()
		self.sorgu()
		self.düzen()
		self.ayarlar()
		

		self.addTab(self.tablo1,'kayıt Bölümü')
		self.addTab(self.tablo2,'Sorgu Bölümü')
		self.addTab(self.tablo3,'Veri Silme ve Düzenleme Bölümü')
		self.addTab(self.tablo4,'Ayarlar')


		self.show()

	def kayıt(self):

		self.title = QLineEdit()
		self.title.setPlaceholderText('Başlık')
		self.title.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))
		self.title.setAlignment(Qt.AlignCenter)		

		self.side = QLineEdit()
		self.side.setPlaceholderText('Yan Başlık')
		self.side.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))
		self.side.setAlignment(Qt.AlignCenter)	

		self.save_dbname1 = QLineEdit()
		self.save_dbname1.setPlaceholderText('Hangi Tabloya Kayıt Edicekseniz.')
		self.save_dbname1.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))

		self.error = QLineEdit()
		self.error.setPlaceholderText('Error Kısmı')
		self.error.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))
		self.error.setReadOnly(True)

		self.data1 = QTextEdit()
		self.data1.setPlaceholderText('Veri Bölümü 1')
		self.data1.setAlignment(Qt.AlignCenter)
		self.data1.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))

		self.data2 = QTextEdit()
		self.data2.setPlaceholderText('Veri Bölümü 2')
		self.data2.setAlignment(Qt.AlignCenter)
		self.data2.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))

		self.send = QPushButton('Kaydet')		
		self.send.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))
		self.send.clicked.connect(self.sql)

		self.clear1 = QPushButton('Temizle')
		self.clear1.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))
		self.clear1.clicked.connect(self.clear)

		form = QFormLayout()
		h_box = QHBoxLayout()
		v_box = QVBoxLayout()

		h_box.addWidget(self.title)
		h_box.addWidget(self.side)

		v_box.addWidget(self.data1)
		v_box.addWidget(self.data2)

		form.addRow(self.save_dbname1)
		form.addRow(h_box)
		form.addRow(v_box)
		form.addRow(self.error)
		form.addRow(self.send)
		form.addRow(self.clear1)

		self.tablo1.setLayout(form)

	def sorgu(self):
		
		self.selection = QComboBox()
		self.selection.addItems(['Başlığa Göre Ara','Yan Başlığa Göre Ara','Çift Arama','İçeriğe Göre Arama'])
		self.selection.setToolTip('Arama Seçeniğidir.')

		self.info = QPushButton()
		self.info.setIcon(QIcon('info.png'))

		self.search1 = QLineEdit()
		self.search1.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))
		self.search1.setStyleSheet('color:darkcyan')
		self.search1.setPlaceholderText('Başlık')

		self.search2 = QLineEdit()
		self.search2.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))		
		self.search2.setStyleSheet('color:darkcyan')
		self.search2.setPlaceholderText('Yan Başlık')

		self.search3 = QLineEdit()
		self.search3.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))		
		self.search3.setStyleSheet('color:darkcyan')
		self.search3.setPlaceholderText('İçeriğe Göre Arama Kısmı')

		self.all = QPushButton('Bütün Veri tabanını getir.')
		self.all.setFont(QFont('Arial',12,QFont.StyleItalic))
		self.all.clicked.connect(self.all_connected)

		#bring = getir		
		self.bring = QPushButton('Getir')
		self.bring.setFont(QFont('Arial',12,QFont.StyleItalic))
		self.bring.clicked.connect(self.search)

		self.clear2 = QPushButton('Temizle')
		self.clear2.setFont(QFont('Arial',12,QFont.StyleItalic))
		self.clear2.clicked.connect(self.clears)

		self.output = QPushButton('Verileri Dışarı Çıkar')
		self.output.setFont(QFont('Arial',12,QFont.StyleItalic))
		self.output.clicked.connect(self.outputs)

		self.read = QTextEdit()
		self.read.setReadOnly(True)
		self.read.setFont(QFont('Arial',12,QFont.StyleItalic))
		self.read.setMinimumSize(600,350)

		self.warning = QLineEdit('')
		self.warning.setReadOnly(True)
		self.warning.setFont(QFont('Arial',16,QFont.StyleItalic))

		form = QFormLayout()
		h_box = QHBoxLayout()
		h_box2 = QHBoxLayout()
		h_box3 = QHBoxLayout()

		h_box.addWidget(self.selection)
		h_box.addWidget(self.info)

		h_box2.addWidget(self.search1)
		h_box2.addWidget(self.search2)

		h_box3.addWidget(self.all)
		h_box3.addWidget(self.bring)

		form.addRow(h_box)
		form.addRow(h_box2)
		form.addRow(self.search3)
		form.addRow(h_box3)		
		form.addRow(self.output)
		form.addRow(self.clear2)
		form.addRow(self.warning)
		form.addRow(self.read)

		self.tablo2.setLayout(form)

	def düzen(self):

		self.identify = QComboBox()		

		self.titleEdit = QLineEdit()
		self.titleEdit.setPlaceholderText('Düzenlenecek Başlık')
		self.titleEdit.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))
		self.titleEdit.setAlignment(Qt.AlignCenter)

		self.sideEdit = QLineEdit()
		self.sideEdit.setPlaceholderText('Düzenlenecek Yan Başlık')
		self.sideEdit.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))
		self.sideEdit.setAlignment(Qt.AlignCenter)

		self.data1Edit = QTextEdit()
		self.data1Edit.setPlaceholderText('Düzenlenecek Veri Bölümü 1')
		self.data1Edit.setAlignment(Qt.AlignCenter)
		self.data1Edit.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))

		self.data2Edit = QTextEdit()
		self.data2Edit.setPlaceholderText('Düzenlenecek Veri Bölümü 2')
		self.data2Edit.setAlignment(Qt.AlignCenter)
		self.data2Edit.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))

		self.err = QTextEdit()
		self.err.setReadOnly(True)
		self.err.setFont(QFont('Arial',14.5,QFont.Bold,QFont.StyleItalic))
		self.err.setMaximumSize(950,75)
		

		self.getir = QPushButton('Getir')
		self.getir.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))
		self.getir.clicked.connect(self.edition)

		self.save = QPushButton('Kaydet')
		self.save.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))
		self.save.clicked.connect(self.saves)

		self.clear3 = QPushButton('Temizle')		
		self.clear3.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))
		self.clear3.clicked.connect(self.clears3)

		self.delete = QPushButton('Veri Silme Bölümü')
		self.delete.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))
		self.delete.clicked.connect(self.sorgu_sil)

		self.yenile = QPushButton()
		self.yenile.setIcon(QIcon('refresh.png'))
		self.yenile.clicked.connect(self.refresh)

		self.form = QFormLayout()
		h_box = QHBoxLayout()
		h_box2 = QHBoxLayout()
		h_box3 = QHBoxLayout()
		h_box4 = QHBoxLayout()


		h_box.addWidget(self.titleEdit)
		h_box.addWidget(self.sideEdit)

		h_box2.addWidget(self.identify)
		h_box2.addWidget(self.yenile)

		h_box3.addWidget(self.getir)
		h_box3.addWidget(self.save)

		h_box4.addWidget(self.clear3)
		h_box4.addWidget(self.delete)

		self.form.addRow(h_box2)
		self.form.addRow(h_box)
		self.form.addRow(self.data1Edit)
		self.form.addRow(self.data2Edit)
		self.form.addRow(self.err)
		self.form.addRow(h_box3)
		self.form.addRow(h_box4)

		self.tablo3.setLayout(self.form)

	def ayarlar(self):

		self.changeme_db = QLineEdit()
		self.changeme_db.setFont(QFont('Arial',17,QFont.Bold,QFont.StyleItalic))

		self.changeme_dbtext = QLabel('Veritabanı Adını Değiştirin')
		self.changeme_dbtext.setFont(QFont('Arial',17,QFont.StyleItalic))

		self.changeme_table = QLineEdit()
		self.changeme_table.setFont(QFont('Arial',17,QFont.StyleItalic))

		self.changeme_tabletext = QLabel('Veritabanına Yeni Tablo Adı Ekleyin')
		self.changeme_tabletext.setFont(QFont('Arial',17,QFont.StyleItalic))

		self.msg_err = QTextEdit()
		self.msg_err.setFont(QFont('Arial',17,QFont.StyleItalic))

		self.db_seclectiontext = QLabel('Veritabanı Adını Seç')
		self.db_seclectiontext.setFont(QFont('Arial',17,QFont.StyleItalic))

		self.db_seclection = QLineEdit()
		self.db_seclection.setFont(QFont('Arial',17,QFont.StyleItalic))

		self.db_seclectionbtn = QPushButton('Veritabanı Adını Seç')
		self.db_seclectionbtn.setFont(QFont('Arial',16,QFont.StyleItalic))
		self.db_seclectionbtn.clicked.connect(self.db_select)

		self.table_selectiontext = QLabel('Veritabanı Tablo Adını Seç')
		self.table_selectiontext.setFont(QFont('Arial',17,QFont.StyleItalic))

		self.table_selection = QLineEdit()
		self.table_selection.setFont(QFont('Arial',16,QFont.StyleItalic))

		self.table_selectionbtn = QPushButton('Veritabanı Tablo Seç')
		self.table_selectionbtn.setFont(QFont('Arial',17,QFont.StyleItalic))
		self.table_selectionbtn.clicked.connect(self.tableselect)

		self.new_db = QPushButton('Yeni Veritabanı Oluştur')
		self.new_db.setFont(QFont('Arial',17,QFont.StyleItalic))
		self.new_db.clicked.connect(self.new_database)

		self.addtable = QPushButton('Yeni Tablo Oluştur')
		self.addtable.setFont(QFont('Arial',17,QFont.StyleItalic))
		self.addtable.clicked.connect(self.add_newtable)

		self.tablo = QPushButton('Tablo Listele')		
		self.tablo.setFont(QFont('Arial',16,QFont.Bold,QFont.StyleItalic))
		self.tablo.clicked.connect(self.tablolistele)		

		form = QFormLayout()
		h_box = QHBoxLayout()
		h_box2 = QHBoxLayout()

		h_box.addWidget(self.new_db)
		h_box.addWidget(self.addtable)
		
		h_box2.addWidget(self.db_seclectionbtn)
		h_box2.addWidget(self.table_selectionbtn)

		form.addRow(self.changeme_dbtext)
		form.addRow(self.changeme_db)
		form.addRow(self.changeme_tabletext)
		form.addRow(self.changeme_table)
		form.addRow(self.table_selectiontext)
		form.addRow(self.table_selection)		
		form.addRow(self.db_seclectiontext)
		form.addRow(self.db_seclection)
		form.addRow(h_box)
		form.addRow(h_box2)
		form.addRow(self.tablo)
		form.addRow(self.msg_err)

		self.tablo4.setLayout(form)

	# Ayarlar Start

	def db_select(self):
		try:
			if len(self.db_seclection.text()) > 1:
				del self.dbname
				self.dbname = self.db_seclection.text()
				self.con = sql.Connection(self.dbname)
				self.csr = self.con.cursor()
				self.csr.execute('CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY,title TEXT,side TEXT,data1 TEXT,data2 TEXT)'.format(self.tablename))
				self.con.commit()
		except Exception as e:
			self.msg_err.setText('Err : ' + str(e))


	def tableselect(self):
		try:
			if len(self.table_selection.text()) > 1:				
				self.tablename = self.table_selection.text()
				self.csr.execute('select * from {}'.format(self.tablename))
		except Exception as e:
			self.msg_err.setText('ERR :  Yanlış Veritabanı Adı')
		print('table : ' + self.tablename)

	def new_database(self):
		if len(self.changeme_db.text()) > 0:

			self.dbname = self.changeme_db.text()
			if len(self.changeme_table.text()) > 1:
				a = str(self.changeme_table.text()).split()
				print(a)
				if len(a) > 1:
					self.tablename = ''
					for i in a:
						self.tablename = self.tablename + i + '_'

					if self.tablename.endswith('_'):
						self.tablename = self.tablename[0:-1]
						print(self.tablename)
				else:
					self.tablename = self.changeme_table.text()					
				
				del self.con;del self.csr
				self.con = sql.Connection(self.dbname)
				self.csr = self.con.cursor()
				self.csr.execute('CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY,title TEXT,side TEXT,data1 TEXT,data2 TEXT)'.format(self.tablename))
				self.msg_err.setText('Veritabanı Başarılı Bir Şekilde Eklendi...')
			else:
			# Veritabanı adı girilipte tablo ismi girilmezse tablename değişmeden {} adında bir tablo oluştursun demek istiyorum.
				self.csr.execute('CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY,title TEXT,side TEXT,data1 TEXT,data2 TEXT)'.format(self.tablename))
		else:
			self.msg_err.setText('Lütfen Tüm Form Alanlarını Doldurunuz...')

	def add_newtable(self):

		print(self.changeme_table.text())
		if len(self.changeme_table.text()) > 1:
			self.tablename = self.changeme_table.text()
			# tablename değiştirmemin sebebi global olup diğer fonksiyonlardaki işlemleri eklemesinden dolayıdır.
			self.csr.execute('CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY,title TEXT,side TEXT,data1 TEXT,data2 TEXT)'.format(self.tablename))
			self.msg_err.setText('Tablo Başarılı Bir Şekilde Eklendi...')
		else:
			self.msg_err.setText('Lütfen Bir Tablo Adı Giriniz.')

	def tablolistele(self):
		print(self.tablename)
		self.csr.execute("select name from sqlite_master where type='table'")
		self.datas = self.csr.fetchall()
		self.msg_err.setText('Veritabanı Adı : ' + str(self.dbname) + '\nTabloların Adı :  ' + str(self.tablename) + '\n')
		for i in self.datas:
			self.msg_err.setText(self.msg_err.toPlainText() + ' | ' + i[0])
		self.msg_err.setText(self.msg_err.toPlainText() + ' | ')

	# Ayarlar Stop

	# Kayıt method start 
	def sql(self):
		try:
			if len(self.save_dbname1.text()) >= 1:
				try:
					self.tablename = self.save_dbname1.text()
					self.csr.execute('select id from {}'.format(self.tablename))
				except Exception as e:
					self.err.setText('VeriTabanı Tablosuna bağlanılamadı ')
				else:
					if len(self.title.text()) >= 1 and len(self.side.text()) >= 1 and len(self.data1.toPlainText()) >= 1 and len(self.data2.toPlainText()) >= 1:
						self.csr.execute('INSERT INTO {} (title,side,data1,data2) VALUES ("{}","{}","{}","{}")'.format(self.tablename,self.title.text().strip().lower().title(),self.side.text().strip().lower().title(),self.data1.toPlainText().strip().lower().title(),self.data2.toPlainText().strip().lower().title()))
						self.con.commit()
					elif len(self.title.text()) >= 1 and len(self.side.text()) >= 1 and len(self.data1.toPlainText()) >= 1:
						print(self.title.text(),self.side.text(),self.data1.toPlainText(),sep="\t")
						self.csr.execute('INSERT INTO {} (title,side,data1,data2) VALUES ("{}","{}","{}","{}")'.format(self.tablename,self.title.text().strip().lower().title(),self.side.text().strip().lower().title(),self.data1.toPlainText().strip().lower().title(),''))
						self.con.commit()
					elif len(self.title.text()) >= 1 and len(self.side.text()) >= 1 and len(self.data2.toPlainText()) >= 1:
						print(self.title.text(),self.side.text(),self.data1.toPlainText(),sep="\t")
						self.csr.execute("INSERT INTO {} (title,side,data1,data2) VALUES ('{}','{}','{}','{}')".format(self.tablename,self.title.text().strip().lower().title(),self.side.text().strip().lower().title(),self.data2.toPlainText().strip().lower().title(),''))
						self.con.commit()					
					elif len(self.title.text()) >= 1 and len(self.data1.toPlainText()) >= 1:
						self.csr.execute('INSERT INTO {} (title,side,data1,data2) VALUES ("{}","{}","{}","{}")'.format(self.tablename,self.title.text().strip().lower().title(),'',self.data1.toPlainText().strip().lower().title(),''))
						self.con.commit()
					elif len(self.title.text()) >= 1 and len(self.data2.toPlainText()) >= 1:
						self.csr.execute('INSERT INTO {} (title,side,data1,data2) VALUES ("{}","{}","{}","{}")'.format(self.tablename,self.title.text().strip().lower().title(),'',self.data2.toPlainText().strip().lower().title(),''))
						self.con.commit()
					else:
						self.error.setText('en az bir girdi olmalı')
					self.con.commit()
		except IndexError as e:
			self.error.setText(str(e))
		else:
			self.error.setText('Bir Hata ile Karşılaşılmadı')			

	def clear(self):
		self.title.setText('')
		self.side.setText('')
		self.data1.setText('')
		self.data2.setText('')
		self.error.setText('Form Alanları Temizlendi')

	# Kayıt method stop 

    # Sorgu method start

	def all_connected(self):
		try:
			self.csr.execute('select * from {}'.format(self.tablename))
			self.datas = self.csr.fetchall()
			print(self.datas)

			for i in self.datas:
				self.read.setText(self.read.toPlainText() + "\nID\n" + str(i[0]) + "\n")
				self.read.setText(self.read.toPlainText() + "\nTITLE\n" + i[1] + "\n")
				self.read.setText(self.read.toPlainText() + "\nSIDE\n" + i[2] + "\n")
				self.read.setText(self.read.toPlainText() + "\nDATA1\n" + i[3] + "\n")
				self.read.setText(self.read.toPlainText() + "\nDATA2\n" + i[4] + "\n\n")
				self.read.setText(self.read.toPlainText() + "\n" + "-"*113)

			self.warning.setText('Veriler Başarılı Bir Şekilde Okundu...')


		except IndexError as e:
			self.warning.setText('Veriler Okunamadı\n' + str(e))

	def search(self):

		try:
			self.proc = []
			self.out_point = False
			print(self.selection.currentText())

			if self.selection.currentText() == 'Başlığa Göre Ara':
				if len(self.search1.text()) > 1:
					self.csr.execute('select * from {} where title="{}"'.format(self.tablename,self.search1.text().lower().title()))
					self.datas = self.csr.fetchall()


					if len(self.datas) > 1:
						for i in self.datas:
							self.read.setText(self.read.toPlainText() + "\nID\n" + str(i[0]) + "\n")
							self.read.setText(self.read.toPlainText() + "\nTITLE\n" + i[1] + "\n")
							self.read.setText(self.read.toPlainText() + "\nSIDE\n" + i[2] + "\n")
							self.read.setText(self.read.toPlainText() + "\nDATA1\n" + i[3] + "\n")
							self.read.setText(self.read.toPlainText() + "\nDATA2\n" + i[4] + "\n\n")
							self.read.setText(self.read.toPlainText() + "\n" + "-"*113)
						self.out_point = True

					elif len(self.datas) == 1:						
						for i in self.datas:
							self.read.setText(self.read.toPlainText() + "\nID\n" + str(i[0]) + "\n")
							self.read.setText(self.read.toPlainText() + "\nTITLE\n" + i[1] + "\n")
							self.read.setText(self.read.toPlainText() + "\nSIDE\n" + i[2] + "\n")
							self.read.setText(self.read.toPlainText() + "\nDATA1\n" + i[3] + "\n")
							self.read.setText(self.read.toPlainText() + "\nDATA2\n" + i[4] + "\n\n")
							self.read.setText(self.read.toPlainText() + "\n" + "-"*113)
						self.out_point = True

					else:
						self.csr.execute('select *from {} where title like "%{}%"'.format(self.tablename,self.search1.text().lower().title()))
						self.datas = self.csr.fetchall()

						if len(self.datas) > 1:
							for i in self.datas:
								self.read.setText(self.read.toPlainText() + "\nID\n" + str(i[0]) + "\n")
								self.read.setText(self.read.toPlainText() + "\nTITLE\n" + i[1] + "\n")
								self.read.setText(self.read.toPlainText() + "\nSIDE\n" + i[2] + "\n")
								self.read.setText(self.read.toPlainText() + "\nDATA1\n" + i[3] + "\n")
								self.read.setText(self.read.toPlainText() + "\nDATA2\n" + i[4] + "\n\n")
								self.read.setText(self.read.toPlainText() + "\n" + "-"*113)
							self.out_point = True

						else:
							for i in self.datas:
								self.read.setText(self.read.toPlainText() + "\nID\n" + str(i[0]) + "\n")
								self.read.setText(self.read.toPlainText() + "\nTITLE\n" + i[1] + "\n")
								self.read.setText(self.read.toPlainText() + "\nSIDE\n" + i[2] + "\n")
								self.read.setText(self.read.toPlainText() + "\nDATA1\n" + i[3] + "\n")
								self.read.setText(self.read.toPlainText() + "\nDATA2\n" + i[4] + "\n\n")
								self.read.setText(self.read.toPlainText() + "\n" + "-"*113)
							self.out_point = True


			elif self.selection.currentText() == 'Yan Başlığa Göre Ara':
				if len(self.search2.text()) > 1:
					self.csr.execute('select * from {} where side="{}"'.format(self.tablename,self.search2.text().lower().title()))
					self.datas = self.csr.fetchall()

					if len(self.datas) > 1:
						self.read.setText(self.read.toPlainText() + "\n")
						for i in self.datas:
							self.read.setText(self.read.toPlainText() + "\nID\n" + str(i[0]) + "\n")
							self.read.setText(self.read.toPlainText() + "\nTITLE\n" + i[1] + "\n")
							self.read.setText(self.read.toPlainText() + "\nSIDE\n" + i[2] + "\n")
							self.read.setText(self.read.toPlainText() + "\nDATA1\n" + i[3] + "\n")
							self.read.setText(self.read.toPlainText() + "\nDATA2\n" + i[4] + "\n\n")
							self.read.setText(self.read.toPlainText() + "\n" + "-"*113)
						self.out_point = True

					elif len(self.datas) == 1:
						self.read.setText(self.read.toPlainText() + "\n\n")
						for i in self.datas:
							self.read.setText(self.read.toPlainText() + "\nID\n" + str(i[0]) + "\n")
							self.read.setText(self.read.toPlainText() + "\nTITLE\n" + i[1] + "\n")
							self.read.setText(self.read.toPlainText() + "\nSIDE\n" + i[2] + "\n")
							self.read.setText(self.read.toPlainText() + "\nDATA1\n" + i[3] + "\n")
							self.read.setText(self.read.toPlainText() + "\nDATA2\n" + i[4] + "\n\n")
							self.read.setText(self.read.toPlainText() + "\n" + "-"*113)
						self.out_point = True	
					else:
						self.csr.execute('select * from {} where side like "%{}%"'.format(self.tablename,self.search2.text().lower().title()))
						self.datas = self.csr.fetchall()

						if len(self.datas) > 1:
							for i in self.datas:
								self.read.setText(self.read.toPlainText() + "\nID\n" + str(i[0]) + "\n")
								self.read.setText(self.read.toPlainText() + "\nTITLE\n" + i[1] + "\n")
								self.read.setText(self.read.toPlainText() + "\nSIDE\n" + i[2] + "\n")
								self.read.setText(self.read.toPlainText() + "\nDATA1\n" + i[3] + "\n")
								self.read.setText(self.read.toPlainText() + "\nDATA2\n" + i[4] + "\n\n")
								self.read.setText(self.read.toPlainText() + "\n" + "-"*113)
							self.out_point = True	

						else:
							for i in self.datas:
								self.read.setText(self.read.toPlainText() + "\nID\n" + str(i[0]) + "\n")
								self.read.setText(self.read.toPlainText() + "\nTITLE\n" + i[1] + "\n")
								self.read.setText(self.read.toPlainText() + "\nSIDE\n" + i[2] + "\n")
								self.read.setText(self.read.toPlainText() + "\nDATA1\n" + i[3] + "\n")
								self.read.setText(self.read.toPlainText() + "\nDATA2\n" + i[4] + "\n\n")
								self.read.setText(self.read.toPlainText() + "\n" + "-"*113)
							self.out_point = True

			elif self.selection.currentText() == 'Çift Arama':
				if len(self.search1.text()) > 1 and len(self.search2.text()) > 1:
					self.csr.execute('select * from {} where title like "%{}%" union all select * from {} where side like "%{}%"'.format(self.tablename,self.search1.text().lower().title(),self.tablename,self.search2.text().lower().title()))
					self.datas = self.csr.fetchall()

					for i in self.datas:
						self.read.setText(self.read.toPlainText() + "\nID\n" + str(i[0]) + "\n")
						self.read.setText(self.read.toPlainText() + "\nTITLE\n" + i[1] + "\n")
						self.read.setText(self.read.toPlainText() + "\nSIDE\n" + i[2] + "\n")
						self.read.setText(self.read.toPlainText() + "\nDATA1\n" + i[3] + "\n")
						self.read.setText(self.read.toPlainText() + "\nDATA2\n" + i[4] + "\n\n")
						self.read.setText(self.read.toPlainText() + "\n" + "-"*113)
					self.out_point = True	

			elif self.selection.currentText() == 'İçeriğe Göre Arama':
				self.csr.execute('select * from {} where data1 or data2 like "%{}%"'.format(self.tablename,self.search3.text().lower().title()))
				self.datas = self.csr.fetchall()
				for i in self.datas:
					self.read.setText(self.read.toPlainText() + "\nID\n" + str(i[0]) + "\n")
					self.read.setText(self.read.toPlainText() + "\nTITLE\n" + i[1] + "\n")
					self.read.setText(self.read.toPlainText() + "\nSIDE\n" + i[2] + "\n")
					self.read.setText(self.read.toPlainText() + "\nDATA1\n" + i[3] + "\n")
					self.read.setText(self.read.toPlainText() + "\nDATA2\n" + i[4] + "\n\n")
					self.read.setText(self.read.toPlainText() + "\n" + "-"*113)
				self.out_point = True

			else:
				self.warning.setText('')
				self.out_point = False
		except ValueError as e:
			self.read.setText(e)

	def clears(self):
		self.search1.setText('')
		self.search2.setText('')
		self.search3.setText('')
		self.read.setText('')
		self.warning.setText('Form Alanları Temizlendi')

	def outputs(self):
		# read
		fsave = QFileDialog.getSaveFileName(self,'Dosyayı Kaydet','save.csv','csv,txt')
		print(fsave)

		if fsave[0][-3:].lower() == 'csv':
			print('csv file online')

			with open(fsave[0],'a') as fopen:
				csv_writer = csv.writer(fopen,delimiter=',')				
				if True:
					for i in self.datas:
						csv_writer.writerow(i)
				else:
					self.read.setText(self.read.toPlainText() + '\nVeri Bulunamadı')

	# Sorgu method stop

	# Düzen method start

	def saves(self):
		if len(self.titleEdit.text()) >= 1 and len(self.sideEdit.text()) >= 1 and len(self.data1Edit.toPlainText()) >= 1 and len(self.data2Edit.toPlainText()) >= 1:
			self.csr.execute('''UPDATE {} SET title="{}",side="{}",data1="{}",data2="{}" WHERE id="{}"'''.format(self.tablename,self.titleEdit.text().strip().title(),self.sideEdit.text().strip().title(),self.data1Edit.toPlainText().replace("\"","\'").strip().title(),self.data2Edit.toPlainText().replace("\"","\'").strip().title(),self.identify.currentText()))
			self.con.commit()
		else:
			
			selection_list = ['Evet Değişiklikleri Kaydet...','Hayır Değişiklikleri Kaydetme...']
			selection,booling = QInputDialog.getItem(self,'Seçim Araçı','Boş olan form alanı tespit edildi.'.title(),selection_list,0,False)

			if booling:
				if selection[0].lower() == 'e':
					self.csr.execute('''UPDATE {} SET title="{}",side="{}",data1="{}",data2="{}" WHERE id="{}"'''.format(self.tablename,self.titleEdit.text().strip().title(),self.sideEdit.text().strip().title(),self.data1Edit.toPlainText().replace("\"","\'").strip().title(),self.data2Edit.toPlainText().replace("\"","\'").strip().title(),self.identify.currentText()))
					self.con.commit()

	def edition(self):
		try:
			self.csr.execute('select * from {} where id="{}"'.format(self.tablename,self.identify.currentText()))
			self.datas = self.csr.fetchall()

			self.titleEdit.setText(self.datas[0][1])
			self.sideEdit.setText(self.datas[0][2])
			self.data1Edit.setText(self.datas[0][3])
			self.data2Edit.setText(self.datas[0][4])
		except IndexError as e:
			self.err.setText('{} Numaralı kayıt Silinmiş Olabilir...'.format(self.identify.currentText()))
		except Exception as e:
			self.err.setText('Err :\n{}\n{}'.format(sys.exc_info()[0],sys.exc_info()[1]))

	def clears3(self):
		self.titleEdit.setText('')
		self.sideEdit.setText('')
		self.data1Edit.setText('')
		self.data2Edit.setText('')
		self.err.setText('') 

	def refresh(self):
		self.csr.execute('select * from {}'.format(self.tablename))
		self.identify.clear()
		self.identify.addItems([str(i[0]) for i in self.csr.fetchall()])

	def sorgu_sil(self):
		self.csr.execute('select id from {}'.format(self.tablename))
		sql_del,booling = QInputDialog.getItem(self,'Veri Silme Bölümü','Hangi Veriyi Silicekseniz ID Numarasını Seçiniz',[str(i[0]) for i in self.csr.fetchall()],0,False)

		if booling:
			try:
				self.csr.execute('DELETE FROM {} where id = "{}"'.format(self.tablename,sql_del))
				self.con.commit()
				self.err.setText(self.err.toPlainText() + '\n{} Numaralı Kayıt Başarıyla Silindi'.format(sql_del) )
			except Exception as e:
				self.err.setText(self.err.toPlainText() + '\n' + str(e))

	# Düzen method start



if __name__ == '__main__':
	app = QApplication(sys.argv)	
	window = Main()
	sys.exit(app.exec_())

