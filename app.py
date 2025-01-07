from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)
data = pd.read_csv('cleaned_data.csv')
pickle_in = open('RigdeModel.pkl', 'rb')
pipe = pickle.load(pickle_in)

@app.route('/')
def index():
    location = sorted(data['location'].unique())
    return render_template('index.html', location=location)

@app.route('/predict', methods=['POST'])
def predict():
    location = request.form.get('location')
    bhk = float(request.form.get('bhk'))
    bath = float(request.form.get('bath'))  
    sqft = float(request.form.get('sqft'))
    print(location, bhk, bath, sqft)
    input = pd.DataFrame([[location, bhk, bath, sqft]], columns=['location', 'bhk', 'bath', 'total_sqft'])
    prediction = pipe.predict(input)[0] * 1e5
    result = "The predicted price is " + str(np.round(prediction, 2))
    return result

if __name__ == '__main__':
    app.run(debug=True, port=8080)
