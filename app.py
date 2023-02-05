import os

from flask import Flask, request, jsonify, redirect, render_template, send_from_directory
from flask_apscheduler import APScheduler
import requests
from nostr.key import PublicKey
from dao import get_publickey_by_name, set_publickey_by_name, get_name_by_publickey

assets_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "assets")
templates_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

SYSTEM_DOMAIN = 'nostr.workfun.life'


class Config(object):
    SCHEDULER_API_ENABLED = True


app = Flask('app')
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

name_map = {
    'master': '7b67d9a61d9d087050a4a202c7c8286cd6e95863ebc7cb6161cc78a732684b69',
}


@scheduler.task('interval',
                id='keep_alive',
                seconds=60,
                misfire_grace_time=900)
def keep_alive():
    print('keep alive')
    r = requests.get(
        'https://nostr.lnanddj.repl.co/.well-known/nostr.json?name=master')
    print(r.json())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory(assets_root, path)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(templates_root, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/api/username/<username>/-/action/check', methods=['GET'])
def check_username(username):
    print(username)
    if get_publickey_by_name(username):
        data = {'status': 'registered'}
    else:
        data = {'status': 'ok'}
    return jsonify(data)


@app.route('/api/publickey/<public_key>/-/action/check', methods=['GET'])
def check_public_key(public_key):
    if not public_key:
        return jsonify({'status': 'parameter error'})
    hex_public_key = covert_public_key_to_hex(public_key)
    if hex_public_key is None:
        data = {'status': 'format_error'}
    else:
        name = get_name_by_publickey(hex_public_key)
        if name:
            data = {'status': 'registered', 'username': name}
        else:
            data = {'status': 'ok'}
    return jsonify(data)


def covert_public_key_to_hex(public_key):
    if public_key.startswith('npub'):
        try:
            pb = PublicKey.from_npub(public_key)
        except Exception as e:
            print(e)
            return None
        return pb.hex()
    return None


@app.route('/api/verify', methods=['POST'])
def verify():
    req = request.get_json()
    if not req:
        return jsonify({'status': 'parameter error'})
    username = req.get('username')
    public_key = req.get('public_key')
    if not username or not public_key:
        return jsonify({'status': 'parameter error'})
    hex_public_key = covert_public_key_to_hex(public_key)
    if hex_public_key is None:
        return jsonify({'status': 'format_error'})
    if get_publickey_by_name(username):
        return jsonify({'status': 'registered'})
    if get_name_by_publickey(hex_public_key):
        return jsonify({'status': 'registered'})

    set_publickey_by_name(username, hex_public_key)
    data = {'status': 'ok', 'nip05': f'{username}@{SYSTEM_DOMAIN}'}
    return jsonify(data)


@app.route('/.well-known/nostr.json')
def verification():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "name parameter is required"})

    hex_public_key = get_name_by_publickey(name)
    if not hex_public_key:
        return jsonify({"error": "name not found"})
    data = {'names': {name: hex_public_key}}
    return jsonify(data)


@app.route('/<path:u_path>')
def redirect1(u_path):
    print(u_path)
    return redirect(
        "https://file-examples.com/storage/feeb72b10363daaeba4c0c9/2017/04/file_example_MP4_1920_18MG.mp4",
        code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
