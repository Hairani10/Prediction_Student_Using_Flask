from flask import Flask, request, render_template, redirect, url_for
import pickle
import pymysql.cursors, os

app = Flask(__name__)

model_svm = pickle.load(open('model_svm.pkl', 'rb'))

conn = cursor = None
#Fungsi Koneksi Database
def konekDb():
	global conn, cursor
	conn = pymysql.connect(host = 'localhost',
							user = 'root',
							password = '',
							database = 'db_prediksi',
							charset = 'utf8mb4',
							cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor()

#fungsi tutup koneksi DB	
def tutupDb():
	global conn,cursor
	cursor.close()
	conn.close()
	
@app.route('/')
def index():
	konekDb()
	list = []
	sql = 'Select * from mahasiswa'
	cursor.execute(sql)
	results = cursor.fetchall()
	for data in results:
		list.append(data)
	tutupDb()
	return render_template('index.html', list=list)

@app.route('/predict', methods=['POST','GET'])
def predict():

	JK, IPS1, IPS2, IPS3, IPS4, IPS5 = [x for x in request.form.values()]
	data = []
	

	if JK == 'Laki-laki':
		data.extend([0])
	else:
		data.extend([1])
		

	data.append(float(IPS1))
	data.append(float(IPS2))
	data.append(float(IPS3))
	
	data.append(float(IPS4))
	
	data.append(float(IPS5))
	    
	status = model_svm.predict([data])
	
	konekDb()
	sql = "INSERT INTO mahasiswa (JK, IPS1,IPS2, IPS3, IPS4, IPS5, status) VALUES (%s, %s, %s,%s, %s, %s, %s)"
	val = (JK, IPS1, IPS2, IPS3, IPS4, IPS5, status)
	cursor.execute(sql, val)
	conn.commit()
	tutupDb()
	return redirect(url_for('index'))

@app.route('/hapus/<JK>', methods=['GET','POST'])
def hapus(JK):
   konekDb()
   cursor.execute('DELETE FROM mahasiswa WHERE JK=%s', (JK,))
   conn.commit()
   tutupDb()
   return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)