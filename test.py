import re

def get_user_name(command: str, user_info: str ):

    regex_name = r'[a-zA-ZА-Яа-я]+'
    user_input_split = user_info.strip().split()
    name_list =[]
    for i in user_input_split:
        match_name = re.match(regex_name, i)
        if match_name:
            if len(match_name.group()) == len(i): # checking if there are no other symbols than letters
                name_list.append(i.capitalize())
                user_info = user_info[match_name.span()[1]:].strip()
                phone = user_info
            else:
                print ('\nName is not correct! Try again!')
                break
        
        if len(name_list)>=1:
            name = ' '.join(name_list)
            print (name, phone)
        
        else:
            print ('\nName is not correct! Try again!')
            break
    print (name, phone)
    return name, phone

if __name__ == '__main__':

    command = 'phone'
    user_info = 'Иванов Иван Иванович +380(67)999-1-777'
    print (get_user_name(command, user_info))