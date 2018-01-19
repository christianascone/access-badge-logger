#!/bin/bash

# Loading users configuration

function log_date() {
    echo "$(date +%Y-%m-%d)"
}

function log_access() {
    printf "$1 > $2\r\n" >> "$log_path""/luna_$(log_date).log"
    # printf "\r\n" >> "$log_path""/luna_$(log_date).log"
}

function log_i() {
  printf "$1\n"
}

function log_w() {
    log_i "$1"
}

function log_e() {
    log_i "$1"
}


log_i "Booting upsystem"

# configs
log_path="./Accessi"
config_path="./Config"
users_file="${config_path}/users.conf"

log_i "Loading users..."

users=()
i=0


if [ ! -f "${users_file}" ]; then
    log_e "Errore caricamento configurazione"
    exit
fi

while read line
do
    # Check empty line
    [[ $line == '' ]] && continue
    
    # Reading user at index $i
    users[$i]=$line
    let i++
done < "${users_file}"

log_i "Loaded $i users"

log_i "System ok."

while :
do
    read -e -a access_code -p "Access > " -r -s

    c_date="$(date)"

    logged_user="$(grep "^$access_code:" "${users_file}")"

    [[ "$logged_user" == '' ]] && log_w 'Utente non trovato. Riprova' && 
continue

    user=$(echo "$logged_user" | cut -d":" -f2)
    gender_value=$(echo "$logged_user" | cut -d":" -f3 | cut -c 1)
    echo =$user=
    echo =$gender_value=
    if [[ $gender_value == "F" ]]; then
        gender="a"
    else
        gender="o"
    fi
    log_i "\n"
    log_i "$c_date: Bentornat$gender $user"
    log_i ""
    log_access "$(date +%Y-%m-%d\ %H:%M:%S)" "$access_code - $user"

done
