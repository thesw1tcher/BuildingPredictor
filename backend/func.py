import pandas as pd
from datetime import datetime

def str_to_datetime_not_hour(a: str):
  return datetime.strptime(a, "%Y-%m-%d")


def add_season(df: pd.DataFrame, name_of_col: str):
    date = df[name_of_col]

    season = []

    for i in range(len(date)):
        a = date[i]
        pred = a[5:7]
        if pred in ['01', '02', '12']:
            season.append('Зима')
        elif pred in ['03', '04', '05']:
            season.append('Весна')
        elif pred in ['06', '07', '08']:
            season.append('Лето')
        else:
            season.append('Осень')

    return season

