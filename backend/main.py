from flask import Flask, request, render_template, send_from_directory
import pandas as pd
from catboost import CatBoostRegressor


app = Flask(__name__)

@app.get('/')
def upload():
    return render_template('index.html')


@app.post('/view')
def view():
    file = request.files['file']
    file.save(file.filename)
    data = pd.read_excel(file)

    model = CatBoostRegressor()
    model.load_model('./model/model.cbm', format='cbm')

    return send_from_directory(directory='./backend', filename=file.filename)


app.run('0.0.0.0', port=5000, debug=True)