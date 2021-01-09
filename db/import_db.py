"""csvディレクトリにあるcsvファイルからPostgresにimportする"""
import subprocess


# DB table list
csv_file_names = [
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
def import_csv(path, table_name):
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
        f"\copy {table_name} from {path}{table_name}.csv delimiter ',' csv header; \
        select setval('{table_name}_id_seq', (select max(id) from {table_name}));",  # pkのシーケンスを最大に変更
    ]
    return command


# import csv
for name in csv_file_names:
    command = import_csv(path, name)
    subprocess.run(command)
