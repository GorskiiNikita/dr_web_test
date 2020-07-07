import hashlib
import os

import settings

from flask import Flask, request, send_from_directory


api = Flask(__name__)


@api.route("/files", methods=["POST"])
def post_file():
    try:
        file = request.files['file']
    except KeyError:
        return {'error': "request don't have file"}, 400

    file_raw = file.read()
    file_hash = hashlib.sha256(file_raw).hexdigest()

    try:
        os.mkdir(f'{settings.UPLOAD_DIRECTORY}/{file_hash[:2]}')
    except FileExistsError:
        pass

    with open(f'{settings.UPLOAD_DIRECTORY}/{file_hash[:2]}/{file_hash}', 'wb') as f:
        f.write(file_raw)

    return {'file_hash': file_hash}, 201


@api.route("/files/<string:file_hash>", methods=['GET'])
def get_file(file_hash):
    return send_from_directory(f'{settings.UPLOAD_DIRECTORY}/{file_hash[:2]}', file_hash, as_attachment=True)


@api.route("/files/<string:file_hash>", methods=['DELETE'])
def delete_file(file_hash):
    try:
        os.remove(f'{settings.UPLOAD_DIRECTORY}/{file_hash[:2]}/{file_hash}')
    except FileNotFoundError:
        return {'error': f'No such file - {file_hash}'}, 404

    if not os.listdir(f'{settings.UPLOAD_DIRECTORY}/{file_hash[:2]}'):
        os.rmdir(f'{settings.UPLOAD_DIRECTORY}/{file_hash[:2]}')
    return {'text': f'{file_hash} file has been deleted'}, 200


if __name__ == "__main__":
    api.run(debug=True, port=5001)
