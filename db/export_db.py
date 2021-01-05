"""Postgresからcsvディレクトリにcsvファイルをexportする"""
import os
import subprocess


# DB table list
tables = [
    'custom_user',
    'note',
    'question',
    'tag',
    'note_tag',
    'star',
    'review',
    'follow',
]


# csv path of container_id
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
    # import csv
    for table in tables:
        command = export_csv(path, table)
        subprocess.run(command)
    # get workdir
    workdir = os.path.dirname(os.path.abspath(__file__))
    # run copy
    subprocess.run(['docker', 'cp', f'wordbook_db_1:{path}', workdir])
