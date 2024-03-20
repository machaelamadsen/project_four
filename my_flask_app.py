from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the machine learning model
RegModel = KNeighborsRegressor(n_neighbors=2)

# Load the scaler
scaler = StandardScaler()

# Load the trained model and scaler
wine = pd.read_csv('winequality_red.csv')  # Assuming you have the dataset
Predictors = ['alcohol', 'density']
TargetVariable = 'quality'
X = wine[Predictors].values
y = wine[TargetVariable].values
X_scaled = scaler.fit_transform(X)
RegModel.fit(X_scaled, y)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    alcohol = float(request.form['alcohol'])
    density = float(request.form['density'])
    input_data = np.array([[alcohol, density]])
    input_data_scaled = scaler.transform(input_data)
    prediction = RegModel.predict(input_data_scaled)[0]
    return render_template('result.html', quality=prediction)

if __name__ == '__main__':
    app.run(debug=True)