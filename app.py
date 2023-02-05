from flask import Flask, request, jsonify, redirect, render_template
from flask_apscheduler import APScheduler
import requests


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


@app.route('/api/username/<username>/-/action/check', methods=['GET'])
def check_username(username):
    print(username)
    if username == 'abc':
        data = {'status': 'registered'}
    else:
        data = {'status': 'ok'}
    return jsonify(data)


@app.route('/api/publickey/<public_key>/-/action/check', methods=['GET'])
def check_public_key(public_key):
    print(public_key)
    if public_key == 'abc':
        data = {'status': 'format_error'}
    else:
        data = {'status': 'ok'}
    return jsonify(data)


@app.route('/api/verify', methods=['POST'])
def verify():
    req = request.get_json()
    print(req)
    data = {'status': 'ok', 'nip05': 'master@workfun.life'}
    return jsonify(data)


@app.route('/.well-known/nostr.json')
def verification():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "name parameter is required"})

    public_key = name_map.get(name)
    if not public_key:
        return jsonify({"error": "name not found"})
    data = {'names': {name: public_key}}
    return jsonify(data)


@app.route('/<path:u_path>')
def redirect1(u_path):
    print(u_path)
    return redirect(
        "https://file-examples.com/storage/feeb72b10363daaeba4c0c9/2017/04/file_example_MP4_1920_18MG.mp4",
        code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
