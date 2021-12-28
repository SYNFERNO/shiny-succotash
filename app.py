from flask import Flask, jsonify, request
import hashlib

app = Flask(__name__)

from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'sim_obat'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8889
mysql.init_app(app)

@app.route("/obat/all")
def get_all():
   conn = mysql.connect()
   cur = conn.cursor()
   cur.execute("SELECT * FROM master_obat")
   row_headers=[x[0] for x in cur.description]
   rv = cur.fetchall()
   json_data=[]
   for result in rv:
        json_data.append(dict(zip(row_headers,result)))
   return jsonify(message="Data ditemukan", status=True, data=json_data)

@app.route("/obat/by_id/<id>", methods = ['GET'])
def get_obat_by_id(id):
   conn = mysql.connect()
   cur = conn.cursor()
   query = """SELECT * from master_obat WHERE id = %s"""
   cur.execute(query, (id))
   row_headers=[x[0] for x in cur.description]
   rv = cur.fetchall()
   if(cur.rowcount != 0):
      json_data=[]
      for result in rv:
         json_data.append(dict(zip(row_headers,result)))
      return jsonify(message="Data ditemukan", status=True, data=json_data)
   else:
      return jsonify(message="Data tidak ditemukan", status=False)

@app.route("/pemeriksaan/by_id/<id>", methods = ['GET'])
def get_pemeriksaan_by_id(id):
   conn = mysql.connect()
   cur = conn.cursor()
   query = """SELECT * from pemeriksaan WHERE id = %s"""
   cur.execute(query, (id))
   row_headers=[x[0] for x in cur.description]
   rv = cur.fetchall()
   if(cur.rowcount != 0):
      json_data=[]
      for result in rv:
         json_data.append(dict(zip(row_headers,result)))
      return jsonify(message="Data ditemukan", status=True, data=json_data)
   else:
      return jsonify(message="Data tidak ditemukan", status=False)

@app.route("/pemeriksaan_trx/by_id/<id>", methods = ['GET'])
def get_pemeriksaan_trx_by_id(id):
   conn = mysql.connect()
   cur = conn.cursor()
   query = """SELECT * from pemeriksaan_trx WHERE pemeriksaan_id = %s"""
   cur.execute(query, (id))
   row_headers=[x[0] for x in cur.description]
   rv = cur.fetchall()
   if(cur.rowcount != 0):
      json_data=[]
      for result in rv:
         json_data.append(dict(zip(row_headers,result)))
      return jsonify(message="Data ditemukan", status=True, data=json_data)
   else:
      return jsonify(message="Data tidak ditemukan", status=False)

@app.route("/user/login", methods = ['POST'])
def login():
   conn = mysql.connect()
   _username = request.form['username']
   _password = request.form['password']
   _role_id = request.form['role']
   password_md5 = hashlib.md5(_password.encode('utf-8')).hexdigest()
   conn = mysql.connect()
   cur = conn.cursor()
   query = """SELECT id, username, role FROM user WHERE username = %s AND password = %s AND role = %s"""
   cur.execute(query, (_username, password_md5, _role_id))
   row_headers=[x[0] for x in cur.description]
   rv = cur.fetchall()
   if(cur.rowcount != 0):
      json_data=[]
      for result in rv:
         json_data.append(dict(zip(row_headers,result)))
      return jsonify(message="Login berhasil", status=True, data=json_data)
   else:
      return jsonify(message="Username dan password tidak ditemukan", status=False)

@app.route("/pemeriksaan/obat", methods = ['POST'])
def insert_obat():
   conn = mysql.connect()
   _pemeriksaan_id  = request.form['pemeriksaan_id']
   _obat_id = request.form['obat_id']
   _nama = request.form['nama']
   _indikasi = request.form['indikasi']
   _aturan_pakai = request.form['aturan_pakai']
   _cara_pakai = request.form['cara_pakai']
   _cara_simpan = request.form['cara_simpan']
   _efek_samping = request.form['efek_samping']
   _lama_penggunaan = request.form['lama_penggunaan']
   _interaksi = request.form['interaksi']
   conn = mysql.connect()
   cur = conn.cursor()
   query = """INSERT INTO pemeriksaan_trx (pemeriksaan_id, obat_id, nama, indikasi, aturan_pakai, cara_pakai, cara_simpan, efek_samping, lama_penggunaan, interaksi) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
   cur.execute(query, (_pemeriksaan_id, _obat_id, _nama, _indikasi, _aturan_pakai, _cara_pakai, _cara_simpan, _efek_samping, _lama_penggunaan, _interaksi))
   conn.commit()
   return jsonify(message="Insert data berhasil", status=True)
