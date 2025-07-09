from flask import Flask, render_template, request
import pandas as pd
import joblib
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Load models and feature names
model = joblib.load('model.pkl')
preprocessor = joblib.load('preprocessor.pkl')
feature_names = joblib.load('feature_names.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        temp = float(request.form['temp'])
        rain = float(request.form['rain'])
        snow = float(request.form['snow'])
        weather = request.form['weather']
        date_time = request.form['date_time']
        holiday = request.form['holiday']

        # Process datetime
        dt = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
        hour = dt.hour
        day_of_week = dt.weekday()
        month = dt.month
        is_holiday = 0 if holiday == 'None' else 1

        # Create input dataframe
        input_data = pd.DataFrame({
            'temp': [temp],
            'rain': [rain],
            'snow': [snow],
            'weather': [weather],
            'hour': [hour],
            'day_of_week': [day_of_week],
            'month': [month],
            'is_holiday': [is_holiday]
        })

        # Make prediction
        prediction = model.predict(input_data)[0]

        # Determine which template to render based on traffic volume
        if prediction > 4000:  # Threshold for high traffic
            return render_template('chance.html', prediction=round(prediction))
        else:
            return render_template('nochance.html', prediction=round(prediction))

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)