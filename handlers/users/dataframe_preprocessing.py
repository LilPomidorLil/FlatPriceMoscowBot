import pandas as pd
import numpy as np
import re
from geopy import distance

def read_csv():
    df = pd.read_csv('DataFrameFlat.csv')
    return df

def append_square_flat(df):
    square_flat = []
    name_flat_list = []
    name_flat_list = list(df['flat_name'])
    for i in range(len(name_flat_list)):
        square_flat.append(name_flat_list[i].split(', ')[1].replace('м²', '').strip())
    df['square'] = square_flat
    return df, name_flat_list

def append_count_room(df, name_flat_list):
    count_room = []  # сюда будет записывать площадь
    for i in range(len(name_flat_list)):
        room_list = []
        room_list = list(name_flat_list[i])
        if room_list[0].isdigit():
            count_room.append(room_list[0])
        elif room_list[0] == 'С' or room_list[0] == 'А':
            count_room.append('0')
        else: 
            count_room.append('7')
    df['count_room'] = count_room
    return df



def append_type_housing(df, name_flat_list):
    type_list = []
    type_housing = []
    for i in range(len(name_flat_list)):
        type_list.append(name_flat_list[i].split(',')[0].split('.'))
    for j in range(len(name_flat_list)):
        try:
            type_housing.append(type_list[j][1].strip().capitalize())
        except IndexError:
            if list(type_list[j][0])[0] == 'С':
                type_housing.append('Студия')
            else:
                type_housing.append('Квартира')
    df['type_of_housing'] = type_housing
    return df

def append_district(df):
    name_district_list = []
    district_list = []
    name_district_list = list(df['district'])
    for i in range(len(name_district_list)):
        try:
            district_list.append(name_district_list[i].split('р-н ')[1])
        except IndexError:
            district_list.append(name_district_list[i].split('р-н ')[0].split(' ')[0])  
    
    df['district'] = district_list
    return df


def join_year_house(df):
    year_house = list(df['Построен'])
    house_year = list(df['Год постройки'])
    for i in range(df['Построен'].shape[0]):
        if year_house[i] == house_year[i]:
            pass
        else:
            year_house[i] == house_year[i]
    df['built_house'] = year_house
    return df

def separation_bathroom(df):
    bathroom_list = list(df['Санузел'])
    separation_bathroom = []

    for i in range(len(bathroom_list)):
        try:
            digit_list = re.findall(r'\d+', bathroom_list[i])
            if len(digit_list) == 2:
                separation_bathroom.append(int(digit_list[0]) + int(digit_list[1]))
            else:
                separation_bathroom.append(int(digit_list[0]))  
        except TypeError:
            separation_bathroom.append(1)
    df['bathroom'] = separation_bathroom
    return df

def summ_lift(df):
    lift_list = list(df['Лифты'])
    summ_lift = []
    for i in range(len(lift_list)):
        try:
            digit_list = re.findall(r'\d+', lift_list[i])
            if len(digit_list) == 2:
                summ_lift.append(int(digit_list[0]) + int(digit_list[1]))
            if len(digit_list) == 1:
                summ_lift.append(int(digit_list[0]))
            if len(digit_list) == 0:
                summ_lift.append(int(1))      
        except TypeError:
            summ_lift.append(int(1))
    df['elevators'] = summ_lift
    return df


def one_floor(df):
    floor_list = list(df['Этаж'])
    one_floor_list = []
    for i in range(len(floor_list)):
        one_floor_list.append(re.findall(r'\d+', floor_list[i])[0])
    df['floor'] = one_floor_list
    return df

def sum_balkon(df):
    balkon_list = list(df['Балкон/лоджия'])
    sum_balkon = []
    for i in range(len(balkon_list)):
        try:
            digit_list = re.findall(r'\d+', balkon_list[i])
            if len(digit_list) == 2:
                sum_balkon.append(int(digit_list[0]) + int(digit_list[1]))
            else:
                sum_balkon.append(int(digit_list[0]))
        except TypeError:
            sum_balkon.append(int(0))
    df['balcony'] = sum_balkon
    return df

def house_list_clean(df):
    df['house'].fillna('10', inplace=True)
    house_list = list(df['house'])
    house_list_ready = []
    for i in range(df['house'].shape[0]):
        str_house_list = list(house_list[i])
        for j in range(len(str_house_list)-1):
            if str_house_list[j] == 'к' or str_house_list[j] == 'с' or str_house_list[j] == 'К' or str_house_list[j] == 'С':
                str_house_list.pop(j)
                for k in range(j, len(str_house_list)):
                    str_house_list.pop(j)
                break
        house_list_ready.append(''.join(str_house_list))
    df['house'] = house_list_ready
    return df

def fillna(df):
    df['built_house'] = df['built_house'].fillna('2000')
    df['repair_flat'] = df['Ремонт'].fillna('Косметический')
    df['view_outside'] = df['Вид из окон'].fillna('На улицу')
    df['type_house'] = df['Тип дома'].fillna('Монолитный')
    df['parking'] = df['Парковка'].fillna('Открытая')
    return df


def dist_kreml(df):
    kreml_dist_list = []
    kreml = (55.752004, 37.617734)
    for i in range(df.shape[0]):
        kreml_dist_list.append(distance.distance(df['coord'][i], kreml).km)
    df['dist_kreml'] = kreml_dist_list
    return df

def circle(df):
    if float(df['lat'])<=55.7888532 and float(df['lat'])>=55.7014943:
        df['circle'] = ['Бульварное' if x<1.500 else 'Садовое' if 1.5000<=x<3.000 else '3 Транспортное' if 3.000<=x<6.0000 else 'В пределах МКАД' if 6.000<=x<14 else 'За МКАД'  for x in df['dist_kreml']]
    else:
        df['circle'] = ['Бульварное' if x<1.500 else 'Садовое' if 1.5000<=x<3.000 else '3 Транспортное' if 3.000<=x<6.0000 else 'В пределах МКАД' if 6.000<=x<17 else 'За МКАД'  for x in df['dist_kreml']]
    return df

def get_dummy(df):
    df_dummy = pd.get_dummies(df[['okrug','district','type_of_housing','repair_flat','view_outside','type_house','parking','circle']])
    df = pd.concat([df, df_dummy], axis = 1)
    return df

def data_df(df):
    data = df['price']
    return data

def run_preprocessing_script():
    df = read_csv()
    df = append_square_flat(df)[0]
    df = append_count_room(df, append_square_flat(df)[1])
    df = append_type_housing(df, append_square_flat(df)[1])
    df = append_district(df)
    df = join_year_house(df)
    df = separation_bathroom(df)
    df = summ_lift(df)
    df = one_floor(df)
    df = sum_balkon(df)
    df = house_list_clean(df)
    df = fillna(df)
    df = dist_kreml(df)
    df = circle(df)
    df = get_dummy(df)
    data = data_df(df)
    df.to_excel('DataFrame_after_preprocessing.xlsx', index = False)
    data.to_excel('Value_after_preprocessing.xlsx', index = False)    
    df.to_csv('DataFrame_after_preprocessing.csv', index = False)
    data.to_csv('Value_after_preprocessing.csv', index = False)
    
