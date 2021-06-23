#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
from datetime import datetime, date
import os

today = date.today()


def switch(argument):
    switcher = {
        1: "Jan",
        2: "Fev",
        3: "Mar",
        4: "Abr",
        5: "Mai",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Set",
        10: "Out",
        11: "Nov",
        12: "Dez"
    }
    return switcher.get(argument, "")


def get_file_name():
    dias = ('seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom')
    dia = dias[today.weekday()]
    final_name = f'bkup_{dia}.zip'
    return final_name


def rename_backup():
    time = datetime.now()
    now = time.strftime("%p")
    if now == 'AM':
        now = 'mat'
    elif now == 'PM':
        now = 'vesp'
    dias = ('seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom')
    hj = date.today()
    dia = dias[hj.weekday()]
    final_name = dia + "_" + now
    return final_name

BASE_DIR = os.getcwd()
backup_name = get_file_name()
root_path = f"backup/{today.year}/{switch(today.month)}-" \
            f"{str(today.month).zfill(2)if len(str(today.month)) else str(today.month)}"
dynamic_filename = f"{switch(today.month)}-{str(today.month).zfill(2)if len(str(today.month)) else str(today.month)}"
GDRIVE_CLIENT_SECRETS_JSON = os.path.join(BASE_DIR, "credenciais/cleiton/client_secrets.json")
GDRIVE_CREDENTIALS_JSON = os.path.join(BASE_DIR, "credenciais/cleiton/credentials.json")
GDRIVE_ROOT = {
    "backups": [
        {
            "folder_path": "backup",
            "files": ["bkup_seg.zip", f"{backup_name}"]
        },
        {
            "folder_path": root_path,
            "files": [f'{dynamic_filename}-nfce.zip', f'{dynamic_filename}-nfe.zip', f'{dynamic_filename}-xml.zip']
        }
    ]
}
