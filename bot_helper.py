"""Напишіть консольного бота помічника, який розпізнаватиме команди, що вводяться з клавіатури, і відповідати відповідно до введеної команди.

Бот помічник повинен стати для нас прототипом застосунку-асистента. Застосунок-асистент в першому наближенні повинен вміти працювати з книгою контактів і календарем. У цій домашній роботі зосередимося на інтерфейсі самого бота. Найпростіший і найзручніший на початковому етапі розробки інтерфейс - це консольний застосунок CLI (Command Line Interface). CLI достатньо просто реалізувати. Будь-який CLI складається з трьох основних елементів:

Парсер команд. Частина, яка відповідає за розбір введених користувачем рядків, виділення з рядка ключових слів та модифікаторів команд.
Функції обробники команд — набір функцій, які ще називають handler, вони відповідають за безпосереднє виконання команд.
Цикл запит-відповідь. Ця частина застосунку відповідає за отримання від користувача даних та повернення користувачеві відповіді від функції-handlerа.
На першому етапі наш бот-асистент повинен вміти зберігати ім'я та номер телефону, знаходити номер телефону за ім'ям, змінювати записаний номер телефону, виводити в консоль всі записи, які зберіг. Щоб реалізувати таку нескладну логіку, скористаємося словником. У словнику будемо зберігати ім'я користувача як ключ і номер телефону як значення.

Умови
Бот повинен перебувати в нескінченному циклі, чекаючи команди користувача.
Бот завершує свою роботу, якщо зустрічає слова: "good bye", "close", "exit".
Бот не чутливий до регістру введених команд.
Бот приймає команди:
"hello", відповідає у консоль "How can I help you?"
"add ...". За цією командою бот зберігає у пам'яті (у словнику наприклад) новий контакт. Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл.
"change ..." За цією командою бот зберігає в пам'яті новий номер телефону існуючого контакту. Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл.
"phone ...." За цією командою бот виводить у консоль номер телефону для зазначеного контакту. Замість ... користувач вводить ім'я контакту, чий номер потрібно показати.
"show all". За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.
"good bye", "close", "exit" за будь-якою з цих команд бот завершує свою роботу після того, як виведе у консоль "Good bye!".
Всі помилки введення користувача повинні оброблятися за допомогою декоратора input_error. Цей декоратор відповідає за повернення користувачеві повідомлень типу "Enter user name", "Give me name and phone please" тощо. Декоратор input_error повинен обробляти винятки, що виникають у функціях-handler (KeyError, ValueError, IndexError) та повертати відповідну відповідь користувачеві.
Логіка команд реалізована в окремих функціях і ці функції приймають на вхід один або декілька рядків та повертають рядок.
Вся логіка взаємодії з користувачем реалізована у функції main, всі print та input відбуваються тільки там."""

import re
import sys

USER_DATA_DICTIONARY = {}


def input_error():# function decorator
    while True:
        try:
            user_input = input ('\nPlease enter command: ') # type str

            if user_input.lower() in ('good bye', 'close', 'exit'):
                print ('\nGood bye! Have a nice day!\n')
                exit()

        except (KeyError, ValueError, IndexError):
            print ('\nWrong input! Try againe!\n')
            continue

        return user_input

def identify_command(input:str, dict: dict):

    for operator, func in dict.items():

        if input == operator:
            return func()

    else:
        print (f'\nUnknown command! Try again!')
        return main()
       
def hello():
    print ('\nHow can I help you?\n')
    return main()

def add():
    user_input =  input ("\nEnter the name and phone number in the next format:\n\nName Surname +380(11)111-1-1 or '+380(11)111-11-11\n\n>>>")
    regex_name = r'[a-zA-Z]+'
    regex_phone = regex = r'\+380\(\d{2}\)\d{3}\-\d{1}\-\d{3}|\+380\(\d{2}\)\d{3}\-\d{2}\-\d{2}'
    match_name = re.findall(regex_name, user_input)
    if not match_name:
        print ("Name is not correct! Try againe!")
        return add()
    name =' '.join(match_name)
    print (name)
    match_phone = re.findall(regex_phone, user_input)
    if not match_phone:
        print ("\nPhone is not correct! Try againe!\n")
        return add()
    phone = match_phone[0]
    print (phone)

    return main()



def give_answer():
    ...

COMMAND_INPUT = {'hello': hello, 'add...': add, 'change...':'Enter user name and new phone please' }
#'phone' : 'The phone for this user is: ', 'show all': 'here all info in my database'}

def main():
    user_input = input_error()
    identify_command(user_input, COMMAND_INPUT)


if __name__ == '__main__':
    main()
#Mykhaylo Ivanov +380(67)282-83-13
#Mykhaylo +380(67)282-83-13
#Mykhaylo +380(67)282-8-313
# +380(67)282-8-313