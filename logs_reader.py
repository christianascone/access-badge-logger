import os

EXPORTS_LOG_FILE = 'exports/logs_csv.csv'
USERS_CONF_DIRECTORY = 'Config/users.conf'
LOGS_DIRECTORY = 'Accessi'

users_dict = dict()
users_file = open(USERS_CONF_DIRECTORY, 'r')
users_list = [user.split(':')[0] for user in users_file]
users_file.close()
arr_txt = [x for x in os.listdir(LOGS_DIRECTORY) if x.endswith('.log')]
csv_filename = EXPORTS_LOG_FILE
if not os.path.exists(os.path.dirname(csv_filename)):
    os.makedirs(os.path.dirname(csv_filename))
# Write CSV
csv_file = open(csv_filename, 'w')
# Empty cell
csv_file.write(';')
[csv_file.write(user_name.strip() + ';') for user_name in sorted(users_list) if user_name]
csv_file.write('\n')
for file_name in arr_txt:
    log_file = open(LOGS_DIRECTORY + '/' + file_name, 'r')
    users_dict = dict()
    for user in users_list:
        users_dict[user] = ''
    for line in log_file:
        if not line.strip():
            continue
        data = line.split(' ')
        if len(data) > 3:
            user_id = data[3]
            hour = data[1]
            users_dict[user_id] = hour

    log_file.close()
    csv_file.write(file_name.replace('.log','') + ';')
    [csv_file.write(users_dict[key] + ';') for key in sorted(users_dict.keys())]
    csv_file.write('\n')

csv_file.close()
