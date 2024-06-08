# -- coding: utf-8 --

import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import joblib

app = Flask(__name__)
model = joblib.load(r"C:\Users\Harsha\Desktop\FULL STACK DATA SCIENCE\DAY-51 MAY - 20\STUDENTS MARKS PREDICTION\students_marks_predictor.pkl")

df = pd.DataFrame()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    global df
    
    input_features = [int(x) for x in request.form.values()]
    features_value = np.array(input_features)
    
    # Validate input hours
    if input_features[0] < 0 or input_features[0] > 24:
        return render_template('index.html', prediction_text='Please enter valid hours between 1 to 24 if you live on the Earth')
    
    output = model.predict([features_value])[0][0].round(2)
    
    # Ensure the predicted output does not exceed 100 marks
    if output > 100:
        output = 100.00
        additional_text = "Orey Nuvu Manishiva Ledha Manavamruganiva ra 12 Gantallu chalavara neeku rojuki so po inka rest thesuko ledha rest in peace ipothav."
    else:
        additional_text = ""
    
    # Input and predicted value store in df then save in csv file
    df = pd.concat([df, pd.DataFrame({'Study Hours': input_features, 'Predicted Output': [output]})], ignore_index=True)
    print(df)
    df.to_csv('smp_data_from_app.csv', index=False)

    return render_template('index.html', prediction_text='You will get [{}%] marks, when you study [{}] hours per day. {}'.format(output, int(features_value[0]), additional_text))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)

#if __name__ == "__main__":
#   app.run(host='0.0.0.0', port=8080)
