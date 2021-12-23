import telebot
from telebot import types;
from random import randint

bot = telebot.TeleBot('5089550679:AAHiiWy5MxrTyVR_czmOXbtvWZx1y0ll3PI');

users = {} #статус пользователя для обработки входящих сообщений
FieldCells = {} #Словарь для клеток поля
Field = None #переменная для обекта клавиатуры

winCells = [ # Здесь описываем все выигрышные позиции
[0,1,2],
[3,4,5],
[6,7,8],

[0,3,6],
[1,4,7],
[2,5,8],

[0,4,8],
[2,4,6]
]


@bot.message_handler(commands=['start']) # отлавливаем команду /start от пользователя
def start_handler(message):
    bot.send_message(message.chat.id, f'*{message.from_user.first_name}*, привет! Это мой телеграм бот для 5 лабораторной работы. Напиши мне /information для ознакомления со всеми функциями', parse_mode= "Markdown")
    #отправляем в диалог c пользователем по message.chat.id текст вставив имея юзера, parse_mode отвечает за стили шрифта (жирный шрифт записывается *text*)
@bot.message_handler(commands=['information'])
def info_handler(message):
    text = "/information - поулчить информацию о боте и командах, /eval - вычислить значение выражения, /tiktactoe - сыграть в Крестики нолики"
    bot.send_message(message.chat.id, text, parse_mode= "Markdown")

@bot.message_handler(commands=['eval'])
def func_handler(message):
    users[message.from_user.id] = 'eval' #задаем для данного юзера по его айди статус eval  \ след сообщение написанное юзером будет отлавливаться на 62 строке
    bot.send_message(message.chat.id, "Используйте знаки 123/41\\*54(20+120)", parse_mode= "Markdown")
    bot.send_message(message.chat.id, "*Введите выражение:*", parse_mode= "Markdown")
@bot.message_handler(commands=['tiktactoe'])
def game_handler(message):
    users[message.from_user.id] = 'tiktactoe'
    global Field #объявляем глобавльную перменную клавиатуры(поля)
    global FieldCells #переенную для клеток поля
    Field = types.InlineKeyboardMarkup(); #создаем клавиатуру
    cell0= types.InlineKeyboardButton(text=' ', callback_data='0'); #создаем каждую клектку поля с текстом " ", пустое поле и колбэк дата для отслеживания айдишника клекти на поле
    cell1= types.InlineKeyboardButton(text=' ', callback_data='1');
    cell2= types.InlineKeyboardButton(text=' ', callback_data='2');
    cell3= types.InlineKeyboardButton(text=' ', callback_data='3');
    cell4= types.InlineKeyboardButton(text=' ', callback_data='4');
    cell5= types.InlineKeyboardButton(text=' ', callback_data='5');
    cell6= types.InlineKeyboardButton(text=' ', callback_data='6');
    cell7= types.InlineKeyboardButton(text=' ', callback_data='7');
    cell8= types.InlineKeyboardButton(text=' ', callback_data='8');
    Field.row(cell0, cell1, cell2) #добавяем клетки поля на каждую строку клавы
    Field.row(cell3, cell4, cell5)
    Field.row(cell6, cell7, cell8)
    FieldCells = {'0':-1, '1':-1,'2':-1, '3':-1, '4':-1,'5':-1, '6':-1, '7':-1,'8':-1, '9': 9} #создаем словарь со всеми клетками и значениями в клетках для данного поля, 10 элесент это кол-во оставшихся клеток
    bot.send_message(message.chat.id, "Ваш ход", parse_mode= "Markdown", reply_markup=Field) #отправляем эту клавиатура вместе с данным сбщ

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if(message.from_user.id in users and users[message.from_user.id] == 'eval'): #если статус пользователя == eval
        if(len(message.text)>0):
            try: #проверка на введеение правильного выражения, если введено слово или другое, то срабатывает ексепт
                bot.send_message(message.chat.id, text=f'Ответ:* ' + str(eval(message.text)) + "*", parse_mode= "Markdown") # команда eval преобразует строковое выражение и считает его
                bot.send_message(message.chat.id, "*Введите выражение:*", parse_mode= "Markdown")
            except Exception as e:
                bot.send_message(message.chat.id, text="Неправильно введено выражение! Попробуйте ещё раз")

def chekWIN(): #проверка выигрышных позиций
    for row in winCells: #проходимся по каждой комбинации выигрышных клеток
        winX = 0 #сколько позиций занимает Х
        winO = 0
        for cell in row: #Проходим по кажлой клетки комбинации
            if ( FieldCells[str(cell)] == 1): winX+=1 #проверяем в нашем поле на данной клетке стоит 1, если да то засчитаываем 1 позициую
            elif ( FieldCells[str(cell)] == 0): winO+=1
        if (winX == 3): #если Х набрал 3 позции на данной комбинации то Х победили
            return 1 #возращаем 1 - победа пользователя
        elif (winO == 3):
            return 0 #победа компьютера
    return -1 #никто не выиграл, играем дальше

def II(): #ход компьюетра
    step = True
    while step: #пока не будет засчитан ход, генерим случайную клетку и проверяем можно ли туда сходить
        ai = randint(0, 8) #клекта для хода от 0 до 8
        for row in Field.keyboard: #смотри каждую строку
            for btn in row: #смотрим каждую клектку данной строки
                if btn.callback_data == str(ai): #если айди клекти == сгенерированной клетки для хода компьютера
                    if(btn.text == " "): #проверяем свободная ли клекта
                        btn.text = "O" #вписываем в дануню клетку О
                        FieldCells[str(ai)] = 0 # в наш словарь с полем тоже заносим изменения после хода
                        FieldCells['9'] = FieldCells['9']-1 # уменьшаем кол-во оставшихся ходов на 1
                        step = False #выходим из цикла
                        break

@bot.callback_query_handler(func=lambda call: True) #обрабатываем нажатия на клавиатуру
def callback_worker(call):
    text = ''
    win = -1 #статус игры
    if(FieldCells['9'] != 0): #если ещё есть клетки для хода
        for row in Field.keyboard:
            for btn in row:
                if btn.callback_data == call.data: #ищим данную клетку по которой нажали сравнив айдишники
                    if(btn.text == " "): #если клетка пустая
                        btn.text = "X" #ставим ход пользователя
                        FieldCells[call.data] = 1 #записываем в наш словарик
                        FieldCells['9'] = FieldCells['9']-1 #уменьшаем кол-во ходов
                        win = chekWIN() #получаем инфу о статусе игры -1, 0 или 1
                        if(win == -1 and FieldCells['9'] != 0): #если никто не выиграл и свободные клетки остались
                            II() #делает ход компьютер
                            win = chekWIN() #снова проверяем не выиграл ли он
                            if(win == -1 and FieldCells['9'] == 0): text="Ничья" #если никто не выиграл и свободные клетки закончились - ничья
                            elif(win == 0): text="Вы проиграли!"; FieldCells['9'] = 0 #если выиграл ПК обнулям свободные клетки чтобы нельзя было больше ходить, и записываем сообщение ля ползвателя
                            else: text="Ваш ход" #если просто никато не выиграл  и есть свободные клетки - выходим из проверок и отправялем собщение пользвоателяю
                        elif (win == 1): text="Вы победили!"; FieldCells['9'] = 0 #если выиграл юзер то записываем сбщ
                        else: text="Ничья" #в ином случае после хода пользователя, образовалась ничья,
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=text, parse_mode= "Markdown", reply_markup=Field) #рдактируем данное сообщение по которому нажали, с помощью айдишника сбщ
    bot.answer_callback_query(call.id) #заканчиваем обработку события

bot.polling(none_stop=True, interval=1); #запускаем бот без перерыва, с задережкой на проверку входящих сообщений размером 1 секунад
