from flask import Flask, request, render_template, send_file
import pandas as pd
from catboost import CatBoostRegressor
from time import time
from datetime import datetime


app = Flask(__name__)

@app.get('/')
def upload():
    return render_template('index.html')


@app.post('/view')
def view():
    file = request.files['file']
    file.save(file.filename)

    data = pd.read_excel(file)
    attr = pd.read_csv('./stat/attr.csv')


    data = data.drop(['№ п/п', 'obj_shortName'], axis=1)


    date = data['ДатаНачалаЗадачи']

    season = []

    for i in range(len(date)):
        try:
            a = str(date[i])
            pred = a[5:7]
            if pred in ['01', '02', '12']:
                season.append('Зима')
            elif pred in ['03', '04', '05']:
                season.append('Весна')
            elif pred in ['06', '07', '08']:
                season.append('Лето')
            else:
                season.append('Осень')
        except TypeError:
            a = str(date[i])

            pred = a[5:7]
            if pred in ['01', '02', '12']:
                season.append('Зима')
            elif pred in ['03', '04', '05']:
                season.append('Весна')
            elif pred in ['06', '07', '08']:
                season.append('Лето')
            else:
                season.append('Осень')

    data['ВремяГодаНачала'] = season

    date = data['ДатаокончанияБП0']

    season = []

    for i in range(len(date)):
        try:
            a = str(date[i])
            pred = a[5:7]
            if pred in ['01', '02', '12']:
                season.append('Зима')
            elif pred in ['03', '04', '05']:
                season.append('Весна')
            elif pred in ['06', '07', '08']:
                season.append('Лето')
            else:
                season.append('Осень')
        except TypeError:
            a = str(date[i])

            pred = a[5:7]
            if pred in ['01', '02', '12']:
                season.append('Зима')
            elif pred in ['03', '04', '05']:
                season.append('Весна')
            elif pred in ['06', '07', '08']:
                season.append('Лето')
            else:
                season.append('Осень')

    data['ВремяГодаОкончанияБП0'] = season
    data = data.drop(['ДатаНачалаЗадачи', 'ДатаОкончанияЗадачи', 'ДатаначалаБП0', 'ДатаокончанияБП0'], axis=1)

    area = []
    for el in data.obj_key:
        area.append(attr[attr['obj_key'] == el]['Площадь'].mean())
    data['area'] = area
    data['area'] = data['area'].fillna(attr['Площадь'].mean())

    data = data.fillna(data.mean(numeric_only=True))
    data = data.fillna(0)

    data.to_excel('./predictions_file/f.xlsx')



    model = CatBoostRegressor()
    model.load_model('./model/model.cbm', format='cbm')

    pred = pd.DataFrame(model.predict(data), columns=['prediction'])

    name = f'./predictions_file/predictions{int(time())}.xlsx'

    pred.to_excel(name)

    return send_file(path_or_file=name, as_attachment=True)


app.run('0.0.0.0', port=5000, debug=True)