import os

EXPORTS_LOG_FILE = 'exports/logs_csv.csv'
USERS_CONF_DIRECTORY = 'Config/users.conf'
LOGS_DIRECTORY = 'Accessi'

# Record indexes
LOG_HOUR_INDEX = 1
LOG_USER_ID_INDEX = 3
LOG_RECORD_MAX_LENGTH = 3


def export_logs_in_csv():
    global users_list, csv_file
    users_file = open(USERS_CONF_DIRECTORY, 'r')
    users_list = [user.split(':')[0] for user in users_file]
    users_file.close()

    def get_log_files_list():
        return [x for x in os.listdir(LOGS_DIRECTORY) if x.endswith('.log')]

    arr_txt = get_log_files_list()
    csv_filename = EXPORTS_LOG_FILE
    if not os.path.exists(os.path.dirname(csv_filename)):
        os.makedirs(os.path.dirname(csv_filename))
    # Write CSV
    csv_file = open(csv_filename, 'w')

    def write_header_row():
        """
        Write the header row with an empty cell and a cell for every user.
        Users' cells are alphabetically sorted.
        :return: void
        """
        # Empty cell for date
        csv_file.write(';')
        [csv_file.write(user_name.strip() + ';') for user_name in sorted(users_list) if user_name]

    write_header_row()
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
            if len(data) > LOG_RECORD_MAX_LENGTH:
                user_id = data[LOG_USER_ID_INDEX]
                hour = data[LOG_HOUR_INDEX]
                users_dict[user_id] = hour

        log_file.close()
        csv_file.write(file_name.replace('.log', '') + ';')
        [csv_file.write(users_dict[key] + ';') for key in sorted(users_dict.keys())]
        csv_file.write('\n')
    csv_file.close()


if __name__ == '__main__':
    print("Starting export...")
    export_logs_in_csv()
    print("Output file in '{0}'".format(EXPORTS_LOG_FILE))