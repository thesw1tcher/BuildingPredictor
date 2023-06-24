from flask import Flask, request, render_template
import pandas as pd


app = Flask(__name__)

@app.get('/')
def upload():
    return render_template('index.html')


@app.post('/view')
def view():
    file = request.files['file']
    file.save(file.filename)
    data = pd.read_excel(file)
    return  data.to_html()


app.run('0.0.0.0', port=5000, debug=True)