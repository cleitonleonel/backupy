#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
from settings import GDRIVE_CLIENT_SECRETS_JSON, \
    GDRIVE_CREDENTIALS_JSON, GDRIVE_ROOT
from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth
import datetime
import sys
import os


class GDriveClient(object):

    def __init__(self, secrets=None, credentials=None):
        super(GDriveClient, self).__init__()
        self.backup_file = None
        self.drive = None
        self.dir = None
        self.service = None
        self.secrets = secrets
        self.credentials = credentials
        authenticator = self.authenticate()
        self.init_drive(authenticator)

    def init_drive(self, authenticator):
        self.drive = GoogleDrive(authenticator)
        self.dir = '/'
        self.service = self.drive.auth.service

    def authenticate(self):
        authenticator = GoogleAuth()
        authenticator.settings = {
            'client_config_backend': 'file',
            'client_config_file': self.secrets,
            'get_refresh_token': True,
            'save_credentials': False,
            'oauth_scope': ['https://www.googleapis.com/auth/drive']
        }

        if self.check_credentials():
            authenticator.LoadCredentialsFile(self.credentials)

        if authenticator.credentials is None:
            response = input('Sem credenciais. Autenticar com o navegador da web local? [s]/n > ')
            if response.lower() in ['s', 'sim'] or len(response) == 0:
                authenticator.LocalWebserverAuth()
            else:
                authenticator.CommandLineAuth()
        elif authenticator.access_token_expired:
            authenticator.Refresh()
        else:
            authenticator.Authorize()

        authenticator.SaveCredentialsFile(self.credentials)
        return authenticator

    def create_backup(self, folder_id, files):
        data = None
        for file in files:
            start_timing_backup = datetime.datetime.now()

            if os.path.exists(file):
                file_name = file
            else:
                print("Nenhum backup encontrado para hoje.")
                sys.exit()

            final_name = os.path.basename(file_name)
            update = self.overwrite_backup(folder_id, final_name)
            if update:
                update.Delete()
            new_file = self.drive.CreateFile(
                {
                    "title": final_name,
                    "parents": [
                        {"kind": "drive#fileLink",
                         "id": folder_id
                         }
                    ]
                }
            )
            new_file.SetContentFile(file_name)
            new_file.Upload()
            print('Upload realizado com sucesso!!!')

            new_file.InsertPermission({
                'type': 'anyone',
                'value': 'anyone',
                'role': 'writer'
            })

            new_file.FetchMetadata(fields='permissions')
            data = {
                'file_name': new_file['title'],
                'link': new_file['webContentLink'],
                'client_modified': new_file['modifiedDate'],
                'size': int(new_file['fileSize']) / 1024
            }
            backup_duration = datetime.datetime.now() - start_timing_backup
            print("Backup gerado em", backup_duration.total_seconds(), "segundos")
        return data

    def check_credentials(self):
        if not os.path.isfile(self.credentials):
            return False
        return True

    def parse_gdrive_path(self, gd_path):
        if ':' in gd_path:
            gd_path = gd_path.split(':')[1]
        gd_path = gd_path.replace('\\', '/').replace('//', '/')
        if gd_path.startswith('/'):
            gd_path = gd_path[1:]
        if gd_path.endswith('/'):
            gd_path = gd_path[:-1]
        return gd_path.split('/')

    def get_folder_list(self, dict_path):
        list_folders = []
        for item in dict_path:
            list_folders.append(self.parse_gdrive_path(item['folder_path']))
        return list_folders

    def create_folder(self, folder_name, parents_id=None):
        metadata = {
            'title': folder_name,
            "mimeType": "application/vnd.google-apps.folder"
        }
        if parents_id:
            metadata["parents"] = [{"id": parents_id}]

        new_folder = self.drive.CreateFile(metadata=metadata)
        new_folder.Upload()
        print('Pasta criada com sucesso!!!')
        print('folder title: %s, id: %s' % (new_folder['title'], new_folder['id']))
        return new_folder['id']

    def prepare_folder(self, folder_list, folder_name, parents=None):
        backup_folder = None
        if not folder_list:
            return self.create_folder(folder_name, parents_id=parents)
        for folder in folder_list:
            if folder['title'] == folder_name:
                backup_folder = folder
                break
            else:
                return self.create_folder(folder_name, parents_id=parents)
        return backup_folder['id']

    def verify_folder(self):
        global folder
        id_folder = None
        list_folders = []
        folder_path = self.get_folder_list(GDRIVE_ROOT["backups"])
        for index, gd_folder in enumerate(folder_path):
            _files = GDRIVE_ROOT["backups"][index]['files']
            if len(gd_folder) > 0:
                id_folder = None
            root = 'root'
            for idx, folder in enumerate(gd_folder):
                folder_list = self.drive.ListFile(
                    {"q": f"'{root}' in parents  and title='{folder}'"
                          f" and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
                id_folder = self.prepare_folder(folder_list, folder, parents=id_folder)
                root = id_folder
            folder_dict = {}
            folder_dict["id"] = id_folder
            folder_dict["name"] = folder
            folder_dict["files"] = _files
            list_folders.append(folder_dict)
        return list_folders

    def overwrite_backup(self, folder, filename):
        file_list = self.drive.ListFile(
            {'q': "'{}' in parents and trashed=false".format(folder)}
        ).GetList()
        if not file_list == []:
            try:
                for file in file_list:
                    if file['title'] == filename:
                        return file
            except ValueError:
                return False
        else:
            return False

    def list_backup(self, folder_id):
        file_list = self.drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
        folder_size = []
        if not file_list == []:
            metadata = []
            for file in file_list:
                folder_size.append(int(file['fileSize']) if file.get('fileSize') else 0)
            folder_size = self.get_size_formatted(sum(folder_size))
            for file in file_list:
                if file.get('fileSize'):
                    file_size = file['fileSize']
                    data = {
                        'file_name': file['title'],
                        'link': file['webContentLink'] if file.get('webContentLink') else '',
                        'client_modified': file['modifiedDate'],
                        'size': self.get_size_formatted(file_size), 'folder_size': folder_size
                    }
                    metadata.append(data)
            return metadata
        else:
            print('Pasta sem arquivos para serem visualizados!!!')
            return False

    @staticmethod
    def get_size_formatted(size):
        global suffix
        total_size = float(f'{int(size) / 1024:.3f}')
        if total_size < 1024:
            total_size = round(float(f'{int(size) / 1024:.2f}'))
            suffix = ' Kb'
        elif total_size >= 1024:
            total_size = round(round(float(f'{int(size) / 1024:.2f}')) / 1024)
            suffix = ' Mb'
        elif total_size >= 1024 * 1024:
            total_size = round(round(float(f'{int(size) / 1024:.2f}')) / 1024)
            suffix = ' Gb'

        return str(total_size) + suffix


if __name__ == '__main__':
    GDrive = GDriveClient(secrets=GDRIVE_CLIENT_SECRETS_JSON,
                          credentials=GDRIVE_CREDENTIALS_JSON
                          )
    folder_ids = GDrive.verify_folder()
    for folder in folder_ids:
        create_backup = GDrive.create_backup(folder_id=folder["id"], files=folder["files"])
        list_files = GDrive.list_backup(folder_id=folder["id"])
        print(f'{folder["name"]}: {list_files}')
