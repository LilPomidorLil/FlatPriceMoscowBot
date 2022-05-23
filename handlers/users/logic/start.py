from aiogram import types
from aiogram.dispatcher.filters import Command
from keyboards.default import menu_first, ml_choice
from loader import dp
from states import MenuButton
from aiogram.dispatcher import FSMContext

from tree import TreeRegressor
from tree import TreeRegressorSlow
from ensemble import BaggingTree
from utils_.saving import save_model

import pandas as pd

from aiogram.utils.markdown import link

@dp.message_handler(Command("start"))
async def show_menu(message: types.Message):
    """
    Начало работы с ботом.
    Описание команды /start
    """

    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=menu_first)
    all_id = pd.read_excel("data_information/all_id.xlsx", index_col=False)
    if message.from_user.id in all_id['id'].to_list():
        return

    new_row = {"id": message.from_user.id}
    all_id = all_id.append(new_row, ignore_index=True)
    all_id.to_excel("data_information/all_id.xlsx", index=False)

@dp.message_handler(text = "Как мною пользоваться?")
async def how_use_me(message: types.Message):
    text = link('Хто я?', 'https://telegra.ph/Kak-menya-yuzat-04-07')
    await message.answer(text,parse_mode="Markdown")


@dp.message_handler(text = "Узнать аренду квартиры! 🤪")
async def choice_ml(message: types.Message):
    await message.answer("*Выберите вариант ввода информации*", parse_mode="Markdown", reply_markup=ml_choice)

@dp.message_handler(Command("send_message"))
async def send_message_start(message: types.Message):
    await message.answer("Введите сообщение, которое необходимо отправить контактам.")
    await MenuButton.set_all_message.set()

@dp.message_handler(state = [MenuButton.set_all_message])
async def send_message_end(message: types.Message, state: FSMContext):
    mess = message.text
    all_id = pd.read_excel("data_information/all_id.xlsx", index_col=False)
    all_id = all_id['id'].to_list()

    for id in all_id:
        await message.bot.send_message(chat_id=id, text = mess, parse_mode="Markdown")

    await state.finish()

##########################################################
###                FITTING - MODEL                     ###
##########################################################
# @dp.message_handler(Command("fit_ml"))
# async def fit_model(message: types.Message):
#     await message.answer("Обучение запущено")
#
#     best_params = {'max_depth': 6, 'min_samples_leaf': 5, 'min_samples_split': 4}
#
#     model = TreeRegressor(**best_params)
#     df = pd.read_csv('Ready_for_fit.csv')
#
#     X = df.drop('price', axis = 1)
#     y = df.price
#     model.fit(X, y)
#
#     save_model(model, 'ML_MODEL/DECISION_TREE_120')
#
#     best_params = {'max_depth': 1, 'min_samples_leaf': 1, 'min_samples_split': 1}
#
#     model = TreeRegressor(**best_params)
#     df = pd.read_csv('Ready_for_fit.csv')
#
#     X = df[df.price < 40000].drop('price', axis=1)
#     y = df[df.price < 40000]['price']
#     model.fit(X, y)
#
#     save_model(model, 'ML_MODEL/DECISION_TREE_40')
#
#     best_params = {'max_depth': 14, 'min_samples_leaf': 3, 'min_samples_split': 1}
#
#     model = TreeRegressorSlow(**best_params)
#     df = pd.read_csv('Ready_for_fit.csv')
#
#     X = df.drop(['price'], axis=1)
#     y = df['price']
#     model.fit(X, y)
#
#     save_model(model, 'ML_MODEL/DECISION_TREE_SLOW_120')
#
#     await message.answer("Деревья обучены")
#
#     model = BaggingTree(base_model=TreeRegressorSlow,
#                         n_estimators=10,
#                         max_depth=14,
#                         min_samples_leaf=3,
#                         min_samples_split=1)
#
#     df = pd.read_csv('Ready_for_fit.csv')
#
#     X = df.drop(['price'], axis=1)
#     y = df['price']
#     model.fit(X, y)
#
#     save_model(model, 'ML_MODEL/BAGGING_TREE_SLOW_120_10')
#
#     model = BaggingTree(base_model=TreeRegressorSlow,
#                         n_estimators=50,
#                         max_depth=14,
#                         min_samples_leaf=3,
#                         min_samples_split=1)
#
#     df = pd.read_csv('Ready_for_fit.csv')
#
#     X = df.drop(['price'], axis=1)
#     y = df['price']
#     model.fit(X, y)
#
#     save_model(model, 'ML_MODEL/BAGGING_TREE_SLOW_120_50')
#
#     model = BaggingTree(base_model=TreeRegressorSlow,
#                         n_estimators=100,
#                         max_depth=14,
#                         min_samples_leaf=3,
#                         min_samples_split=1)
#
#     df = pd.read_csv('Ready_for_fit.csv')
#
#     X = df.drop(['price'], axis=1)
#     y = df['price']
#     model.fit(X, y)
#
#     save_model(model, 'ML_MODEL/BAGGING_TREE_SLOW_120_100')
#
#
#     await message.answer("Модели обучены и готовы к использованию.")

