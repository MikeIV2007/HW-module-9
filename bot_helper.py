# """Напишіть консольного бота помічника, який розпізнаватиме команди, що вводяться з клавіатури, і відповідати відповідно до введеної команди.

# Бот помічник повинен стати для нас прототипом застосунку-асистента. Застосунок-асистент в першому наближенні повинен вміти працювати з книгою контактів і календарем. У цій домашній роботі зосередимося на інтерфейсі самого бота. Найпростіший і найзручніший на початковому етапі розробки інтерфейс - це консольний застосунок CLI (Command Line Interface). CLI достатньо просто реалізувати. Будь-який CLI складається з трьох основних елементів:

# Парсер команд. Частина, яка відповідає за розбір введених користувачем рядків, виділення з рядка ключових слів та модифікаторів команд.
# Функції обробники команд — набір функцій, які ще називають handler, вони відповідають за безпосереднє виконання команд.
# Цикл запит-відповідь. Ця частина застосунку відповідає за отримання від користувача даних та повернення користувачеві відповіді від функції-handlerа.
# На першому етапі наш бот-асистент повинен вміти зберігати ім'я та номер телефону, знаходити номер телефону за ім'ям, змінювати записаний номер телефону, виводити в консоль всі записи, які зберіг. Щоб реалізувати таку нескладну логіку, скористаємося словником. У словнику будемо зберігати ім'я користувача як ключ і номер телефону як значення.

# Умови
# Бот повинен перебувати в нескінченному циклі, чекаючи команди користувача.
# Бот завершує свою роботу, якщо зустрічає слова: "good bye", "close", "exit".
# Бот не чутливий до регістру введених команд.
# Бот приймає команди:
# "hello", відповідає у консоль "How can I help you?"
# "add ...". За цією командою бот зберігає у пам'яті (у словнику наприклад) новий контакт. Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл.
# "change ..." За цією командою бот зберігає в пам'яті новий номер телефону існуючого контакту. Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл.
# "phone ...." За цією командою бот виводить у консоль номер телефону для зазначеного контакту. Замість ... користувач вводить ім'я контакту, чий номер потрібно показати.
# "show all". За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.
# "good bye", "close", "exit" за будь-якою з цих команд бот завершує свою роботу після того, як виведе у консоль "Good bye!".
# Всі помилки введення користувача повинні оброблятися за допомогою декоратора . Цей декоратор відповідає за повернення користувачеві повідомлень типу "Enter user name", "Give me name and phone please" тощо. Декоратор input_error повинен обробляти винятки, що виникають у функціях-handler (KeyError, ValueError, IndexError) та повертати відповідну відповідь користувачеві.
# Логіка команд реалізована в окремих функціях і ці функції приймають на вхід один або декілька рядків та повертають рядок.
# Вся логіка взаємодії з користувачем реалізована у функції main, всі print та input відбуваються тільки там."""

import re
from rich import print
from rich.table import Table

USER_DATA_DICTIONARY = {}

def load_data():
    with open('contacts_log.txt', 'r') as file:
        list = file.readlines()
        if list == []:
            return USER_DATA_DICTIONARY
        else:
            for item in list:
                item_split =item.split(':')
                USER_DATA_DICTIONARY[item_split[0]] = item_split[1].replace('\n', '')
                return USER_DATA_DICTIONARY
             

def save_data():
    with open('contacts_log.txt', 'w') as file:
        for name, phone in USER_DATA_DICTIONARY.items(): 
            file.write(f"{name}:{phone}\n")


def exit_programm_save_dict():
    save_data()
    print ('\nAll data seved to the contacts_log.txt\n\nGood bye! Have a nice day!\n')
    exit()

def add(user_name, phone_number):
    if user_name in USER_DATA_DICTIONARY:
        print (f'\nContat {user_name} is already exist!\nTry other options!')
        main()
    USER_DATA_DICTIONARY[user_name] = phone_number
    print (f'\nNew contat {user_name} {phone_number} added successfully!')
    save_data()
    return main()

def change(user_name, phone_number):
    if user_name not in USER_DATA_DICTIONARY:
        print (f'\nContat {user_name} is already exist!\nTry other options!')
        main()
    USER_DATA_DICTIONARY[user_name] = phone_number
    print (f'\nPhone number {phone_number} for {user_name} changed successfully!')
    save_data()
    return main()

def phone(user_name, phone_number):
    if user_name not in USER_DATA_DICTIONARY:
        print (f'\nContat {user_name} is not exist!\nTry other options!')
        main()
    phone_number = USER_DATA_DICTIONARY[user_name]
    print (f'\n{user_name} phone number is {phone_number}')
    return main()


COMMAND_INPUT = {'add': add, 'change': change, 'phone': phone }
#'add': add(), 'change':'Enter user name and new phone please', 'phone' : 'The phone for this user is: ', 'show all': 'here all info in my database'}

def execute_command(command, user_name, phone_number) -> None:
    COMMAND_INPUT[command](user_name, phone_number)

def input_error(func):
    def wrapper(data):
        try:
            if len(data.split(' '))>=2:
                #print (len(data.split(' ')))
                #print ('OK')
                result = func(data)                

            else:
                print ('\nYour must have at least 2 arguments! Try again!')
                return main()
            
        except(KeyError, ValueError, IndexError, TypeError):
            print ('\nWrong input! Try again\n')
            return main()
        return result
    return wrapper


def pars_user_info(command, user_info ):
    regex_name = r'[a-zA-Z]+'
    regex_phone = regex = r'\+380\(\d{2}\)\d{3}\-\d{1}\-\d{3}|\+380\(\d{2}\)\d{3}\-\d{2}\-\d{2}'
    match_name = re.findall(regex_name, user_info)
    if not match_name:
        
        while True:
            new_name = input("\nName is not correct! Enter correct name!\n\n>>>")
            match_name = re.findall(regex_name, new_name)
            if not match_name:
                continue
            name =' '.join(match_name)
            if name:
                break

    else:
        name =' '.join(match_name)

    if command ==  'phone':
        phone = '+380(11)111-11-11'

    else:
        match_phone = re.findall(regex_phone, user_info)
        if not match_phone:

            while True:
                new_number=input("\nPhone number is not correct!\nEnter phone number in format+380(11)111-1-111 or +380(11)111-11-11!\n\n>>>")
                match_phone = re.findall(regex_phone, new_number)
                #print (match_phone)
                if not match_phone:
                    continue
                phone = match_phone[0]
                #print (phone)
                if phone:
                    #print (phone)
                    break

        else:
            phone = match_phone[0]
            #print (phone)

    return name, phone

@input_error
def identify_command_get_info(input):

    regex_command = r'^[a-zA-Z]+'
    match = re.search(regex_command, input)
    
    if match:
        #print (match)
        command = (match.group()).lower()
        if command in COMMAND_INPUT:
            #print (f'command = {command}')
            span = match.span()
            #print (span)
            user_info = input[span[1]:].strip()
            #print (user_info)
            return command, user_info
    else:
        print ('\nUnknown command! Try agayn!')
        return main()       
        
def get_user_input():
    table_of_commands()
    while True:
        user_input = (input(f"\nEnter command in format according to table above\n\n>>>")).strip()
        if user_input.lower() in ('good bye', 'close', 'exit'):
            #print ('\nGood bye! Have a nice day!\n')
            exit_programm_save_dict()
        if user_input.lower() == 'hello':
            print("How can I help you?")
            continue
        if user_input.lower()== 'show all':
            print (USER_DATA_DICTIONARY)
            continue
        else:
            return user_input
        
def table_of_commands():

    table = Table(title="\nALL VALID COMMANDS AND FORMAT OF DATA\n* - optional ")
    table.add_column("COMMAND", justify="left")
    table.add_column("NAME", justify="center")
    table.add_column("PHONE NUMBER", justify="center")
    table.add_column("DESCRIPTION", justify="left")
    table.add_row('hello', '-', '-', 'Greeting')
    table.add_row('add', 'Name Surname*', '+380(11)111-1-111 or +380(11)111-11-11', 'Add new contact')
    table.add_row('change', 'Name Surname*', '+380(11)111-1-111 or +380(11)111-11-11', 'Change phone number')
    table.add_row('phone', 'Name Surname*', '-', 'Getting phone number')
    table.add_row('show all', '-', '-', 'Getting all database')
    table.add_row('good bye / close / exit', '-', '-', 'Exit') 
   
    return print (table)


def main():
    load_data()
    user_input = get_user_input()
    #print (user_input)
    command, user_info = identify_command_get_info(user_input ) # output is tuple form two values
    #print (command)
    #print (user_info)
    name, phone = pars_user_info(command, user_info)
    #print (name)
    #print (phone)
    execute_command(command, name, phone)

    
if __name__ == "__main__":
    main()

# ADD Bill Jonson +380(67)333-43-54
# ADD Bill +380(67)333-43-54
# ADD Bill Jonson +380(67)333-43-5
# +380(67)282-8-313
# CHange Bill Jonson +380(67)111-41-77
# CHANGE Bill +380(67)454-12-12
# PHONE Bill Jonson
# PHONE Bill
# 12m3m4n
# 12me3m3m 123m3mm2
# ADD Jill Bonson +380(67)333-43-54
# ADD Jill +380(67)333-43-54
# change Jill +380(67)222-33-55
