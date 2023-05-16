from flask import Flask, request, jsonify, send_file, abort
import os
import uuid
from pydub import AudioSegment
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from db import Users, Music, add_user, add_audiofile, find_audiofile, get_audiofile

Base = declarative_base()
engine = create_engine('postgresql://postgres:postgres@db/mp3_web')

app = Flask(__name__)


# Функция конвертер wav to mp3
def convert_wav_to_mp3(input_file: str, output_file: str):
    sound = AudioSegment.from_wav(input_file)
    sound.export(output_file, format="mp3")


# Функция чистит папку audio от временных файлов
def clean_directory():
    folders = ['audio']
    for folder_path in folders:
        # Walk through all subdirectories of the folder and delete each file
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith(('.wav', '.mp3')):
                    file_path = os.path.join(root, file_name)
                    os.remove(file_path)


# Маршрут для создания пользователя
@app.route('/users', methods=['POST'])
def create_user():
    username = request.form['username']
    if len(username) == 0:
        abort(400, 'Username is empty string')
    token = str(uuid.uuid4())  # генератор токена
    user_id = str(uuid.uuid4())  # генератор id
    add_user(username, user_id, token)

    return jsonify({
        'id': user_id,
        'token': token
    })


# Маршрут для добавления аудиозаписи
@app.route('/add_record', methods=['POST'])
def handle_record():
    clean_directory()
    # получение данных из запроса
    user_id = request.form.get('user_id')
    access_token = request.form.get('access_token')
    audio_file = request.files['audio']
    if not user_id or not access_token or not audio_file:
        abort(400, 'Missing parameters')

    # генерация id сохранение аудио файла
    file_uuid = str(uuid.uuid4())
    filename = str(uuid.uuid4()) + '.wav'
    audio_path = os.path.join(app.root_path, 'audio', filename)
    audio_file.save(audio_path)

    # конвертация wav в mp3
    mp3_filename = filename.split('.')[0] + '.mp3'
    mp3_path = os.path.join(app.root_path, 'audio', mp3_filename)
    convert_wav_to_mp3(audio_path, mp3_path)

    # сохранение mp3 в БД
    add_audiofile(file_uuid, mp3_filename)

    # создание URL для загрузки
    download_url = request.host_url + 'record?id=' + file_uuid + '&user=' + user_id

    # возврат URL в ответе пользователю
    return jsonify({'download_url': download_url})


# Маршрут для доступа к аудиозаписи
@app.route('/record', methods=['GET'])
def download_record():
    clean_directory()
    record_id = request.args.get('id')
    user_id = request.args.get('user')
    if not record_id or not user_id:
        abort(400, 'Missing parameters')

    fileinfo = find_audiofile(record_id)
    # Проверка валидности аудиозаписи
    if not fileinfo:
        return 'Неверные учетные данные', 401
    else:
        file = get_audiofile(record_id)
        filename = file['filename']
        filedata = file['filedata']
        with open(f'audio/{filename}', 'wb') as file:
            file.write(filedata)

        headers = {
            'Content-Disposition': f'attachment; filename={filename}',
            'Content-Type': 'audio/mpeg',
        }

        return send_file(f'audio/{filename}', as_attachment=True, download_name=filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
