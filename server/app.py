from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from resource.common import config

def create_app(test_config = None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_profile(config)
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow=0)
    app.database = database
    
    return app

app = create_app()

@app.route("/sing-up", method=['POST'])
def sign_up():
    new_user = request.json
    app.database.execute(f"INSERT INTO users (username, hashed_password, kdnumber) VALUES ('{new_user['name']}', '{new_user['password']}', {new_user['kdnumber']}")
    ##비밀번호 hash 처리하는것, 아이디 중복확인 하는것 추가해야함
    return jsonify(new_user)