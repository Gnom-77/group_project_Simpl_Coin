import telebot
from telebot import types
bot = telebot.TeleBot('7478571974:AAFSUS6TtKrShI5lU346l28C_iq3yFrPyXY')
import psycopg2

try:
    conn = psycopg2.connect(dbname='tg_b', user='postgres', password='123', host='localhost')
except:
    print('Can`t establish connection to database')

with conn.cursor() as curs:
            request = "SELECT technical_name, name, price FROM merch"
            curs.execute(request)
            prices = curs.fetchall()
            request = "SELECT technical_name, name FROM Conditions_for_receiving"
            curs.execute(request)
            achievements = curs.fetchall()
            request = "SELECT id, employees_id, conditions_for_receiving_id, link, date FROM add_coins WHERE order_status_id = 2"
            curs.execute(request)
            addcoins_requests = curs.fetchall()
            request = "SELECT id, employees_id, merch_id, date FROM buying_merch WHERE order_status_id = 2"
            curs.execute(request)
            buying_requests = curs.fetchall()


goodskeys_list = []
dict_to_add = {}
dict_to_buy = {}
dict_chats = {}
with conn.cursor() as curs:
        request = f"SELECT name, chat_id FROM employees"
        curs.execute(request)
        for obj in curs.fetchall():
            dict_chats[obj[0]] = int(obj[1])
            dict_to_add[int(obj[1])] = [0, 0, '', 0]
            dict_to_buy[int(obj[1])] = [0, 0]
for obj in prices:
    name = f"{obj[1]} - {obj[2]}"
    key = types.InlineKeyboardButton(text=name, callback_data=f'buying_{obj[0]}')
    goodskeys_list.append(key)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.username
    with conn.cursor() as curs:
        request = "SELECT role FROM employees WHERE name = '" + str(user_id) + "'"
        curs.execute(request)
        if(curs.fetchone()==None):
            bot.send_message(message.chat.id, text="Вас нет в базе данных.")
            return    
    with conn.cursor() as curs:
        request = f"UPDATE employees SET chat_id = '{message.chat.id}' WHERE name = '{message.from_user.username}'; commit;"
        curs.execute(request)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("HR")
    btn2 = types.KeyboardButton("Сотрудник")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Приветствую, {0.first_name}!  Я бот, позволяющий начислять SimplCoin и обменивать их на различные товары. Для начала выберите свою роль: HR/Сотрудник".format(message.from_user), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    user_id = message.from_user.username
    with conn.cursor() as curs:
        request = "SELECT role FROM employees WHERE name = '" + str(user_id) + "'"
        curs.execute(request)
        if(curs.fetchone()==None):
            bot.send_message(message.chat.id, text="Вас нет в базе данных.")
            return
    if(message.text == "HR"):
        user_id = message.from_user.username
        with conn.cursor() as curs:
            request = "SELECT role FROM employees WHERE name = '" + str(user_id) + "'"
            curs.execute(request)
            user_role = curs.fetchone()[0]
        if (user_role == 'HR'):
            bot.send_message(message.chat.id, text="Авторизация успешна!")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Просмотр заявок на начисление SimplCoin")
            btn2 = types.KeyboardButton("Просмотр заявок на покупку мерча")
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, text="Что бы вы хотели сделать?",  reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text="Отказано в доступе. Если произошла ошибка, обратитесь к администратору.")
    elif(message.text == "Просмотр заявок на начисление SimplCoin"):
        user_id = message.from_user.username
        with conn.cursor() as curs:
            request = "SELECT role FROM employees WHERE name = '" + str(user_id) + "'"
            curs.execute(request)
            user_role = curs.fetchone()[0]
        if (user_role == 'HR'):
            with conn.cursor() as curs:
                global addcoins_requests
                i=0
                for obj in addcoins_requests:
                    request1 = f"SELECT name FROM employees WHERE id = {obj[1]}"
                    curs.execute(request1)
                    employer = curs.fetchone()[0]
                    request1 = f"SELECT name FROM conditions_for_receiving WHERE id = {obj[2]}"
                    curs.execute(request1)
                    condition = curs.fetchone()[0]
                    msg = str(i+1) + ')' +'Сотрудник: ' + str(employer) + ', условие получения: ' + str(condition) + ', ссылка на подтверждение: ' + str(obj[3]) + ', дата создания запроса: ' + str(obj[4]) + '\n'
                    bot.send_message(message.chat.id, text=msg)
                    i=i+1
                i=0
                keyboard = types.InlineKeyboardMarkup(row_width=4)
                keys = []
                for obj in addcoins_requests:
                    key = types.InlineKeyboardButton(text=str(i+1), callback_data=f'addcoinsrequest_{obj[0]}')
                    keys.append(key)
                    i = i + 1
                keyboard.add(*keys)
                bot.send_message(message.chat.id, text="Выберите запрос, который необходимо обработать", reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, text="У вас нет доступа к этому функционалу!")
    elif(message.text == "Просмотр заявок на покупку мерча"):
        user_id = message.from_user.username
        with conn.cursor() as curs:
            request = "SELECT role FROM employees WHERE name = '" + str(user_id) + "'"
            curs.execute(request)
            user_role = curs.fetchone()[0]
        if (user_role == 'HR'):
             with conn.cursor() as curs:
                global buying_requests
                i=0
                for obj in buying_requests:
                    request1 = f"SELECT name FROM employees WHERE id = {obj[1]}"
                    curs.execute(request1)
                    employer = curs.fetchone()[0]
                    request1 = f"SELECT name FROM merch WHERE id = {obj[2]}"
                    curs.execute(request1)
                    merch = curs.fetchone()[0]
                    msg = str(i+1) + ')Сотрудник: ' + str(employer) + ', мерч: ' + str(merch) + ', дата создания запроса: ' + str(obj[3]) + '\n'
                    bot.send_message(message.chat.id, text=msg)
                    i=i+1
                i=0
                keyboard = types.InlineKeyboardMarkup(row_width=4)
                keys = []
                for obj in buying_requests:
                    key = types.InlineKeyboardButton(text=str(i+1), callback_data=f'buyingrequest_{obj[0]}')
                    keys.append(key)
                    i = i + 1
                keyboard.add(*keys)
                bot.send_message(message.chat.id, text="Выберите запрос, который необходимо обработать", reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, text="У вас нет доступа к этому функционалу!")
    elif(message.text == "Сотрудник"):
        user_id = message.from_user.username
        with conn.cursor() as curs:
            request = "SELECT simpl_coin_count FROM employees WHERE name = '" + str(user_id) + "'"
            curs.execute(request)
            flag = curs.fetchone()
           
            if(flag == None):
                bot.send_message(message.chat.id, text="Недостаточно данных. Обратитесь к администратору :)")
            else:
                
                user_balance = flag[0]
                bot.send_message(message.chat.id, text=f"Ваш баланс: {user_balance}")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Создать заявку на начисление SimplCoin")
                btn2 = types.KeyboardButton("Баланс")
                btn3 = types.KeyboardButton("Обменять SimplCoin на товар")
                markup.add(btn1, btn2, btn3)
                bot.send_message(message.chat.id, text="Что бы вы хотели сделать?",  reply_markup=markup)
            
                
    elif(message.text == "Создать заявку на начисление SimplCoin"):
        bot.send_message(message.chat.id, text="Введите username сотрудника без знака '@'")
        bot.register_next_step_handler(message, get_tag)
    elif(message.text == "Обменять SimplCoin на товар"):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for key in goodskeys_list:
            keyboard.add(key)
        bot.send_message(message.chat.id, text="Какой товар вы бы хотели приобрести?", reply_markup=keyboard)
    elif(message.text == "Баланс"):
        user_id = message.from_user.username
        with conn.cursor() as curs:
            request = "SELECT simpl_coin_count FROM employees WHERE name = '" + str(user_id) + "'"
            curs.execute(request)
            user_balance = curs.fetchone()[0]
        bot.send_message(message.chat.id, text=f"Ваш баланс: {user_balance}")

def get_tag(message):
    global dict_to_add
    username = message.text
    with conn.cursor() as curs:
        request = f"SELECT ID FROM employees WHERE name = '{username}'"
        curs.execute(request)
        user = curs.fetchone()
        if(user != None):
            print(f'Словарь: {dict_to_add}')
            for obj in dict_to_add.keys():
                print(type(obj))
            print(message.chat.id)
            print(type(message.chat.id))
            dict_to_add[message.chat.id][0] = user[0]
            bot.send_message(message.chat.id, text="Прикрепите ссылку на подтверждающие фотографии")
            bot.register_next_step_handler(message, get_link)
        else:
            bot.send_message(message.chat.id, text="Такого пользователя не существует. Обратитесь к администратору :) ")     
        
def get_link(message):
    global dict_to_add
    dict_to_add[message.chat.id][2] = message.text
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    msg = "За что начисляются SimplCoin? Выберите цифру"
    i = 1
    keys = []
    for obj in achievements:
        msg =  msg + '\n\n' + str(i) + ')' + obj[1]
        key = types.InlineKeyboardButton(text=str(i), callback_data=f'adding_{obj[0]}')
        keys.append(key)
        i = i + 1
    keyboard.add(*keys)
    bot.send_message(message.chat.id, text=msg, reply_markup=keyboard)

def get_comment_buying(message, buyid):
    with conn.cursor() as curs:
        request = f"UPDATE buying_merch SET hr_comments = '{message.text}' WHERE id = {buyid}; commit;"
        curs.execute(request)
        request1 = f"SELECT employees_id FROM buying_merch WHERE id = {buyid}"
        curs.execute(request1)
        userid = curs.fetchone()[0]
        request1 = f"SELECT name FROM employees WHERE id = {userid}"
        curs.execute(request1)
        username = curs.fetchone()[0]
        request1 = f"SELECT merch_id FROM buying_merch WHERE id = {buyid}"
        curs.execute(request1)
        merchid = curs.fetchone()[0]
        request1 = f"SELECT name FROM merch WHERE id = {merchid}"
        curs.execute(request1)
        merchname = curs.fetchone()[0]
    bot.send_message(message.chat.id, text='Запрос успешно обработан!')
    try:
        bot.send_message(dict_chats[username], f'Ваш запрос на получение мерча "{merchname}" был отклонен. Комментарий: "{message.text}"')
    except:
        print('Чат с пользователем не был найден')
    
def get_comment_adding(message, addid):
    with conn.cursor() as curs:
        request = f"UPDATE add_coins SET hr_comments = '{message.text}' WHERE id = {addid}; commit;"
        curs.execute(request)
        request1 = f"SELECT employees_id FROM add_coins WHERE id = {addid}"
        curs.execute(request1)
        userid = curs.fetchone()[0]
        request1 = f"SELECT name FROM employees WHERE id = {userid}"
        curs.execute(request1)
        username = curs.fetchone()[0]
        request1 = f"SELECT conditions_for_receiving_id FROM add_coins WHERE id = {addid}"
        curs.execute(request1)
        conditionid = curs.fetchone()[0]
        request1 = f"SELECT name FROM conditions_for_receiving WHERE id = {conditionid}"
        curs.execute(request1)
        conditionname = curs.fetchone()[0]
        request = f"SELECT applicant_id FROM add_coins WHERE id = {addid}"
        curs.execute(request)
        applicantid = curs.fetchone()[0]
        request = f"SELECT name FROM employees WHERE id = {applicantid}"
        curs.execute(request)
        applicantname = curs.fetchone()[0]        
    bot.send_message(message.chat.id, text='Запрос успешно обработан!')  
    try:
        bot.send_message(dict_chats[applicantname], f'Ваш запрос на получение SimplCoin за достижение "{conditionname}" для "{username}" был отклонен. Комментарий: "{message.text}"')
    except:
        print('Чат с пользователем не был найден')
def how_much(message, empid, addid):
    global addcoins_requests
    if(not((message.text).isdigit())):
        bot.send_message(message.chat.id, text="Некорректный ввод! Операция отменена!")
    else:
        with conn.cursor() as curs:
            request = f"SELECT applicant_id FROM add_coins WHERE id = {addid}"
            curs.execute(request)
            applicantid = curs.fetchone()[0]
            request = f"SELECT name FROM employees WHERE id = {applicantid}"
            curs.execute(request)
            applicantname = curs.fetchone()[0]
            request = f"UPDATE employees SET simpl_coin_count = simpl_coin_count + {int(message.text)} WHERE id = {empid}"
            curs.execute(request)
            request1 = f"SELECT name FROM employees WHERE id = {empid}"
            curs.execute(request1)
            username = curs.fetchone()[0]
            request1 = f"SELECT conditions_for_receiving_id FROM add_coins WHERE id = {addid}"
            curs.execute(request1)
            conditionid = curs.fetchone()[0]
            request1 = f"SELECT name FROM conditions_for_receiving WHERE id = {conditionid}"
            curs.execute(request1)
            conditionname = curs.fetchone()[0]
            request = f"UPDATE add_coins SET order_status_id = 4 WHERE id = {addid}"
            curs.execute(request)
            request = "SELECT id, employees_id, conditions_for_receiving_id, link, date FROM add_coins WHERE order_status_id = 2"
            curs.execute(request)
            addcoins_requests = curs.fetchall()
        bot.send_message(message.chat.id, text='Запрос успешно обработан!')
        with conn.cursor() as curs:
            request = "commit;"
            curs.execute(request)            
        try:
            bot.send_message(dict_chats[username], f'Вам начислено {message.text} SimplCoin.')
        except:
            print('Чат с пользователем не был найден')

        try:
            bot.send_message(dict_chats[applicantname], f'Ваш запрос на получение SimplCoin за "{conditionname}" для "{username}" был одобрен.')    
        except:
            print(f'Чат с заявителем {applicantname} не был найден')
@bot.callback_query_handler(func=lambda call: True) 
def callback(call):
    req = call.data.split('_')
    global dict_to_add
    global dict_to_buy
    global addcoins_requests
    global buying_requests
    print(req[0])
    if req[0] == 'buying':
        with conn.cursor() as curs:
            request = f"SELECT simpl_coin_count FROM employees WHERE name = '{call.from_user.username}'"
            curs.execute(request)
            balance = curs.fetchone()[0]
        for obj in prices:
            if req[1] == obj[0]:
                with conn.cursor() as curs:
                    techname = obj[0]
                    request = f"SELECT price FROM merch WHERE technical_name = '{techname}'"
                    curs.execute(request)
                    merchprice = curs.fetchone()[0]
                    if(merchprice<balance):
                        request = f"SELECT ID FROM employees WHERE name = '{call.from_user.username}'"
                        curs.execute(request)
                        dict_to_buy[call.message.chat.id][0] = curs.fetchone()[0]
                        request = f"SELECT ID FROM merch WHERE technical_name = '{techname}'"
                        curs.execute(request)
                        dict_to_buy[call.message.chat.id][1] = curs.fetchone()[0]
                        request = f"INSERT INTO buying_merch VALUES (default, {dict_to_buy[call.message.chat.id][0]}, 2, {dict_to_buy[call.message.chat.id][1]}, default); commit;"
                        curs.execute(request)
                        request = "SELECT id, employees_id, merch_id, date FROM buying_merch WHERE order_status_id = 2"
                        curs.execute(request)
                        buying_requests = curs.fetchall()
                        bot.send_message(call.message.chat.id, text="Запрос на получение успешно создан!")
                    else:
                        bot.send_message(call.message.chat.id, text="На вашем счету недостаточно средств для покупки товара.")                        
    elif req[0] == 'adding':
        for obj in achievements:
            if req[1] == obj[0]:
                with conn.cursor() as curs:
                    request = f"SELECT ID FROM conditions_for_receiving WHERE technical_name = '{obj[0]}'"
                    curs.execute(request)
                    dict_to_add[call.message.chat.id][1] = curs.fetchone()[0]
                    request = f"SELECT ID FROM employees WHERE name = '{call.from_user.username}'"
                    curs.execute(request)
                    dict_to_add[call.message.chat.id][3] = curs.fetchone()[0]
                    request = f"INSERT INTO add_coins(id, employees_id, applicant_id, conditions_for_receiving_id, order_status_id, link, date) VALUES (default, {dict_to_add[call.message.chat.id][0]}, {dict_to_add[call.message.chat.id][3]}, {dict_to_add[call.message.chat.id][1]}, 2, '{dict_to_add[call.message.chat.id][2]}', default); commit;"
                    curs.execute(request)
                    request = "SELECT id, employees_id, conditions_for_receiving_id, link, date FROM add_coins WHERE order_status_id = 2"
                    curs.execute(request)
                    addcoins_requests = curs.fetchall()
                    bot.send_message(call.message.chat.id, text="Запрос на получение успешно создан!")
    elif req[0] == 'addcoinsrequest': 
        bot.delete_message(call.message.chat.id, call.message.message_id)         
        for obj in addcoins_requests:
            if req[1] == str(obj[0]):
                with conn.cursor() as curs:
                    request1 = f"SELECT name FROM employees WHERE id = {obj[1]}"
                    curs.execute(request1)
                    employer = curs.fetchone()[0]
                    request1 = f"SELECT name FROM conditions_for_receiving WHERE id = {obj[2]}"
                    curs.execute(request1)
                    condition = curs.fetchone()[0]
                    msg = 'Сотрудник: ' + str(employer) + ', условие получения: ' + str(condition) + ', ссылка на подтверждение: ' + str(obj[3]) + ', дата создания запроса: ' + str(obj[4])
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                key_approved = types.InlineKeyboardButton(text="Одобрить", callback_data=f'addcheck_approved_{obj[0]}')
                key_denied = types.InlineKeyboardButton(text="Отклонить", callback_data=f'addcheck_denied_{obj[0]}')
                key_back = types.InlineKeyboardButton(text="Отмена", callback_data=f'addcheck_back_{obj[0]}')
                keyboard.add(key_approved,key_denied,key_back)
                bot.send_message(call.message.chat.id, text=msg, reply_markup=keyboard)
    elif req[0] == 'buyingrequest': 
        bot.delete_message(call.message.chat.id, call.message.message_id)     
        for obj in buying_requests:
            if req[1] == str(obj[0]):
                with conn.cursor() as curs:
                    request1 = f"SELECT name FROM employees WHERE id = {obj[1]}"
                    curs.execute(request1)
                    employer = curs.fetchone()[0]
                    request1 = f"SELECT name FROM merch WHERE id = {obj[2]}"
                    curs.execute(request1)
                    merch = curs.fetchone()[0]
                    msg = 'Сотрудник: ' + str(employer) + ', мерч: ' + str(merch) + ', дата создания запроса: ' + str(obj[3])
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                key_approved = types.InlineKeyboardButton(text="Одобрить", callback_data=f'buycheck_approved_{obj[0]}')
                key_denied = types.InlineKeyboardButton(text="Отклонить", callback_data=f'buycheck_denied_{obj[0]}')
                key_back = types.InlineKeyboardButton(text="Отмена", callback_data=f'buycheck_back_{obj[0]}')
                keyboard.add(key_approved,key_denied,key_back)
                bot.send_message(call.message.chat.id, text=msg, reply_markup=keyboard)
    elif req[0] == 'addcheck':
        if req[1] == 'approved':
            with conn.cursor() as curs:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                #Начисление коинов на счет
                request = f"SELECT employees_id FROM add_coins WHERE id = {req[2]}"
                curs.execute(request)                
                userid = curs.fetchone()[0]
                bot.send_message(call.message.chat.id, text="Сколько начислить?")
                bot.register_next_step_handler(call.message, how_much, userid, req[2])
        elif req[1] == 'denied':
            with conn.cursor() as curs:
                curruser = call.from_user.username
                request = f"SELECT id FROM employees WHERE name = '{curruser}'"
                curs.execute(request)
                hrid = curs.fetchone()[0]
                request = f"UPDATE add_coins SET order_status_id = 3, hr_id = {hrid} WHERE id = {req[2]}; commit;"
                curs.execute(request)
                request = "SELECT id, employees_id, conditions_for_receiving_id, link, date FROM add_coins WHERE order_status_id = 2"
                curs.execute(request)
                addcoins_requests = curs.fetchall()
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, text="Напишите комментарий")
                bot.register_next_step_handler(call.message, get_comment_adding, req[2])
        elif req[1] == 'back':
            bot.delete_message(call.message.chat.id, call.message.message_id)
    elif req[0] == 'buycheck':
        if req[1] == 'approved':
            with conn.cursor() as curs:
                request = f"UPDATE buying_merch SET order_status_id = 4 WHERE id = {req[2]}"
                curs.execute(request)
                request = "SELECT id, employees_id, merch_id, date FROM buying_merch WHERE order_status_id = 2"
                curs.execute(request)
                buying_requests = curs.fetchall()
                bot.delete_message(call.message.chat.id, call.message.message_id)
                #Списание коинов со счета
                request = f"SELECT merch_id FROM buying_merch WHERE id = {req[2]}"
                curs.execute(request)                
                merchid = curs.fetchone()[0]
                request = f"SELECT price FROM merch WHERE id = {merchid}"
                curs.execute(request)                
                merchprice = curs.fetchone()[0]
                request = f"SELECT employees_id FROM buying_merch WHERE id = {req[2]}"
                curs.execute(request)                
                userid = curs.fetchone()[0]
                request = f"UPDATE employees SET simpl_coin_count = simpl_coin_count - {int(merchprice)} WHERE id = {userid}"
                curs.execute(request)
                request = f"SELECT name FROM employees WHERE id = {userid}"
                curs.execute(request)
                username = curs.fetchone()[0]
                request = f"SELECT name FROM merch WHERE id = {merchid}"
                curs.execute(request)
                merchname = curs.fetchone()[0]
                request = "commit;"
                curs.execute(request)
                bot.send_message(call.message.chat.id, text='Запрос успешно обработан!')    
                try:
                    bot.send_message(dict_chats[username], f'Ваш запрос на получение мерча "{merchname}" был одобрен.')
                except:
                    print('Чат с пользователем не был найден')                
        elif req[1] == 'denied':
            with conn.cursor() as curs:
                curruser = call.from_user.username
                request = f"SELECT id FROM employees WHERE name = '{curruser}'"
                curs.execute(request)
                hrid = curs.fetchone()[0]
                request = f"UPDATE buying_merch SET order_status_id = 3, hr_id = {hrid} WHERE id = {req[2]}; commit;"
                curs.execute(request)
                request = "SELECT id, employees_id, merch_id, date FROM buying_merch WHERE order_status_id = 2"
                curs.execute(request)
                buying_requests = curs.fetchall()
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, text="Напишите комментарий")
                bot.register_next_step_handler(call.message, get_comment_buying, req[2])
        elif req[1] == 'back':
            bot.delete_message(call.message.chat.id, call.message.message_id)

        
if __name__ == '__main__': 
    bot.polling(none_stop=True)