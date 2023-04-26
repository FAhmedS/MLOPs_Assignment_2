import numpy as np
import pandas as pd
import pickle

import requests_file
from flask import *

app = Flask(__name__ , static_url_path='/static')
@app.route('/')
def Home():
    return render_template('index.html')
@app.route('/page2')
def secondPage():
    return render_template('index1.html')
@app.route('/goto_page2')
def goto_page2():
    return redirect(url_for('secondPage'))
@app.route("/predict" , methods = ['POST'])
def predict():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        file_content = uploaded_file.read().decode('utf-8').strip()
        file_contents = file_content.replace('[', '').replace(']', '')
        string_array = file_contents.split(',')
        #print("file_content: " , file_content)
        data = np.array(string_array, dtype=np.float64)
        model = pickle.load(open('model.pkl', 'rb'))
        #data = np.array(file_content)
        print("data1: " , data.dtype ,data.shape)
        data = np.reshape(data, (-1, 23))
        print("data2: ", data.dtype, data.shape)
        asd = model.predict(data)
        print("asd" , asd)
        val = asd[0 , 0]
        if val < 0.50:
            return render_template('index1.html', results="Predicted Value is {:.3f}, Patient is less likely to get Seizure.".format(val))
        else:
            return render_template('index1.html', results= "Predicted Value is {:.3f}, Patient is likely to get Seizure." .format(val))
    else:
        return render_template('index1.html')
if __name__=="__main__":
    app.run(debug=True)