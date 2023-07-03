import re
from rich import print
from rich.table import Table

USER_DATA_DICTIONARY = {}

def not_user_name(func):
    def wrapper(user_name, phone_number):
        if user_name not in USER_DATA_DICTIONARY:
            print (f'\nContat {user_name} is not exist! Try other options!')
            main()
        else:
            func(user_name, phone_number)
    return wrapper

def load_data():
    try:
        with open('contacts_log.txt', 'r') as file:
            list = file.readlines()
            if list == []:
                return USER_DATA_DICTIONARY
            else:
                for item in list:
                    item_split =item.split(':')
                    USER_DATA_DICTIONARY[item_split[0]] = item_split[1].replace('\n', '')
                    return USER_DATA_DICTIONARY
    except FileNotFoundError:
        return None
        

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
        print (f'\nContat {user_name} is already exist! Try other options!')
        main()
    USER_DATA_DICTIONARY[user_name] = phone_number
    print (f'\nNew contat {user_name} {phone_number} added successfully!')
    save_data()
    return main()


@not_user_name
def change(user_name, phone_number):
    USER_DATA_DICTIONARY[user_name] = phone_number
    print (f'\nPhone number {phone_number} for {user_name} changed successfully!')
    save_data()
    return main()

@not_user_name
def phone(user_name, phone_number):
    phone_number = USER_DATA_DICTIONARY[user_name]
    print (f'\n{user_name} phone number is {phone_number}')
    return main()


def show_all():
    with open('contacts_log.txt', 'r') as file:
        list = file.readlines()

    if list == []:
        print ('\nDatabase is empty!')
        return main()
    
    else:
        table = Table(title="ALL CONTACTS IN DATABASE")
        table.add_column("Name", justify="left")
        table.add_column("Phone number", justify="center")

        for item in list:
            item_split =item.split(':')
            table.add_row(item_split[0], item_split[1].replace('\n', ''))
    print (table)
    return main()         


COMMAND_INPUT = {'add': add, 'change': change, 'phone': phone }


def execute_command(command, user_name, phone_number) -> None:
    COMMAND_INPUT[command](user_name, phone_number)


def input_error(func):
    def wrapper(data):
        try:
            regex_command = r'^[a-zA-Z]+'
            match = re.search(regex_command, data)
            
            if match:
                command = (match.group()).lower()

            if command in COMMAND_INPUT:
                span = match.span()
                user_info = data[span[1]:].strip()
                return command, user_info
            
            else:
                print ('\nUnknown command! Try agayn!')
                return main()
                
        except(KeyError, ValueError, IndexError, TypeError, UnboundLocalError):
            print ('\nWrong input! Try again')
            return main()
    return wrapper


def pars_user_info(command, user_info ):
    regex_name = r'[a-zA-ZА-Яа-я]+'
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
                new_number=input("\nPhone number is not correct!\nEnter phone number in format:\n+380(11)111-1-111 or +380(11)111-11-11\n\n>>>")
                match_phone = re.findall(regex_phone, new_number)

                if not match_phone:
                    continue
                phone = match_phone[0]

                if phone:
                    break

        else:
            phone = match_phone[0]


    return name, phone

@input_error
def identify_command_get_info(input):

    regex_command = r'^[a-zA-Z]+'
    match = re.search(regex_command, input)
    
    if match:
        command = (match.group()).lower()

        if command in COMMAND_INPUT:
            span = match.span()
            user_info = input[span[1]:].strip()
            return command, user_info
        
    else:
        print ('\nUnknown command! Try agayn!')
        return main()       
        
def get_user_input():
    table_of_commands()
    while True:
        user_input = (input(f"\nEnter command in format according to the table above\n\n>>>")).strip()
        if user_input.lower() in ('good bye', 'close', 'exit'):
            exit_programm_save_dict()
        if user_input.lower() == 'hello':
            print("How can I help you?")
            continue
        if user_input.lower()== 'show all':
            show_all()
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
    command, user_info = identify_command_get_info(user_input ) # output is tuple form two values
    identify_command_get_info(user_input ) # output is tuple form two values
    name, phone = pars_user_info(command, user_info)
    execute_command(command, name, phone)

    
if __name__ == "__main__":
    main()

#
# ADD Bill Jonson +380(67)333-43-54
# ADD Bill +380(67)333-43-54
# ADD Bill Jonson +380(67)333-43-5
# +380(67)282-8-313
# CHange Mike Jonn +380(67)111-41-77
# PHONE Mike Jonn +380(67)111-41-77
# CHange Bill Jonson +380(67)111-41-77
# CHANGE Bill +380(67)454-12-12
# PHONE Bill Jonson
# PHONE Bill
# 12m3m4n
# 12me3m3m 123m3mm2
# ADD Jill Bonson +380(67)333-43-54
# PhOnE Jill Bonson +380(67)333-43-54
# ADD Jill +380(67)333-43-54
# change Jill +380(67)222-33-55
# Иванов Иван Иванович +380(67)222-33-55
# change Иванов Иван Иванович +380(67)999-1-777
# phone Иванов Иван Иванович 
# dfsadfads asdgfas ref asdf     TypeError
