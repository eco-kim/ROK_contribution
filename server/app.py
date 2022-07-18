from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from resource.common import config
import bcrypt
import jwt
from datetime import datetime, timedelta

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
    new_user['password'] = bcrypt.hashpw(
        new_user['password'].encode('UTF-8'),
        bcrypt.gensalt()
    )
    app.database.execute(f"INSERT INTO users (username, hashed_password, kdnumber) VALUES ('{new_user['username']}', '{new_user['password']}', {new_user['kdnumber']}")
    ##아이디 중복확인 하는것 추가해야함
    return jsonify(new_user)

@app.route("/login", method=['POST'])
def login():
    credential = request.json
    username = credential['username']
    password = credential['password']

    row = app.database.execute(f"SELECT id, hashed_password FROM users WHERE username = '{username}'").fetchone()

    if row and bcrypt.checkpw(password.encode('UTF-8'), row['hashed_password'].encode('UTF-8')):
        user_id = row['id']
        payload = {
            'user_id' : user_id,
            'exp' : datetime.utcnow() + timedelta(seconds = 60*60)
        }
        token = jwt.encode(payload, app.config['JWT_SECRET_KEY'],
        'HS256')
        return jsonify({
            'access_token' : token.decode('UTF-8')
        })
    else:
        return '', 401