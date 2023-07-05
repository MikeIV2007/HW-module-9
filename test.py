import re

regex_name = r'[a-zA-ZА-Яа-я]+'

user_info = 'Jgfdksaflf Sdfjldsf; Asdfk;;lsdff Jldsf;sf;; sdff ; jldsf;sF;;'
user_input_split = user_info.strip().split()
name_list =[]
for i in user_input_split:
    match = re.match(regex_name, i)
    if match:
        if len(match.group()) == len(i): # checking if there are no other symbols than letters
            name_list.append(i.capitalize())
            user_info = user_info[match.span()[1]:].strip()
            phone = user_info
        else:
            print ('\nName is not correct! Try again!')

name = ' '.join(name_list)

print (name)
print (phone)