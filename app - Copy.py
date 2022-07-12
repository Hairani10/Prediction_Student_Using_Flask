from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

model_svm = pickle.load(open('model_svm.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
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
	    
	prediction = model_svm.predict([data])


	return render_template('index.html', Status=prediction, JK=JK, IPS1=IPS1,IPS2=IPS2,IPS3=IPS3,IPS4=IPS4,IPS5=IPS5)


if __name__ == '__main__':
    app.run(debug=True)