"""Postgresからcsvディレクトリにcsvファイルをexportする"""
import os
import subprocess


# DB table list
db_table_names = [
    'custom_user',
    'note',
    'question',
    'tag',
    'note_tag',
    'star',
    'review',
    'follow',
]


# csv directory path
path = '/csv/'


# command
def export_csv(path, table_name):
    """subprocess.runの引数になるリストを返す"""
    command = [
        'docker-compose',
        'exec',
        'db',
        'psql',
        '-d',
        'wordbook',
        '-U',
        'app_owner',
        '-c',
        f"\copy {table_name} to {path}{table_name}.csv delimiter ',' csv header;",
    ]
    return command


if __name__ == '__main__':
    # judge copy
    container = input('hostの/wordbook/db/csv/にコピーする場合は、dbのコンテナIDを入力>>>')
    if container:
        # import csv
        for name in db_table_names:
            command = export_csv(path, name)
            subprocess.run(command)
        subprocess.run(['docker', 'cp', f'{container}:{path}', '.'])
