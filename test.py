import re

regex_name = r'[a-zA-ZА-Яа-я]+'
# regex_phone = regex = r'\+380\(\d{2}\)\d{3}\-\d{1}\-\d{3}|\+380\(\d{2}\)\d{3}\-\d{2}\-\d{2}'
user_info = "Иванов Иван Иванович +380(67)222-33-55"
user_input_strip = user_info.strip().split()
name_list =[]
for i in user_input_strip:
    match = re.match(regex_name, i)
    if match:
        name_list.append(i)
        user_info = user_info[match.span()[1]:].strip()
        phone = user_info
name = ' '.join(name_list)

print (name)
print (phone)
# pattern = r"^(.+?),\s+(\d{3}-\d{3}-\d{4})$"
