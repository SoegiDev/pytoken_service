"""mODULE"""
import json
import datetime
import os
import socket
from flask import Flask, request, jsonify
import jwt
from JSONExceptionHandler import JSONExceptionHandler
app = Flask(__name__)
HOST = "0.0.0.0"
PORT = 5003
if os.environ.get('FLASK_ENV') == 'dev':
    # app.logger.info(os.environ.get('FLASK_ENV'))
    app.config.from_object('config.Development')
elif os.environ.get('FLASK_ENV') == 'testing':
    # app.logger.info(os.environ.get('FLASK_ENV'))
    app.config.from_object('config.Testing')
else:
    # app.logger.info(os.environ.get('FLASK_ENV'))
    app.config.from_object('config.Production')
secret_key = app.config.get('SECRET_KEY')
secret_key_refresh = app.config.get('SECRET_KEY_REFRESH')
expire_token = app.config.get('JWT_ACCESS_TOKEN_EXPIRES')
expired_token_refresh = app.config.get('JWT_REFRESH_TOKEN_EXPIRES')
dict_access = {}
@app.route("/",methods=["GET"])
def home():
    """_summary_
    Returns:
        _type_: _description_
    """
    test=  os.environ.get("FLASK_ENV")
    return f'TOKEN MODE: {test} SOCKETNAME: {socket.gethostname()}'
@app.route("/generate",methods=["POST"])
def generate():
    """_summary_

    Returns:
        _type_: _description_
    """
    payload = json.loads(request.data)
    public_id = payload["id"]
    datauser = {"public_id":public_id}
    token = createtoken(datauser)
    refresh = createrefreshtoken(datauser)
    check_key(dict_access,public_id,0)
    return jsonify({
        "token":token,
        "token_refresh":refresh
    })
def createtoken(datauser : object):
    """_summary_

    Args:
        datauser (object): _description_

    Returns:
        _type_: _description_
    """
    print("Expired ",expire_token)
    token = jwt.encode({
            'id': datauser['public_id'],
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours = int(expire_token))
        }, secret_key, algorithm='HS256')
    return token
def createrefreshtoken(datauser : object):
    """_summary_

    Args:
        datauser (object): _description_

    Returns:
        _type_: _description_
    """
    token = jwt.encode({
            'id': datauser['public_id'],
            'exp' : datetime.datetime.utcnow()\
                + datetime.timedelta(days = int(expired_token_refresh))
        }, secret_key_refresh, algorithm='HS256')
    return token
@app.route("/validate",methods=["POST"])
def validate():
    """_summary_

    Returns:
        _type_: _description_
    """
    payload = json.loads(request.data)
    token = payload["token"]
    public_id = ''
    try:
        # expired_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        jwt_decoded = jwt.decode(token,secret_key, algorithms=["HS256"])
        public_id = jwt_decoded["id"]
        check_key(dict_access,public_id,0)
        return jsonify({
            "id":jwt_decoded["id"]
        }), 200
    except ZeroDivisionError:
        initcheck = False
        initcheck = check_key(dict_access,public_id,1)
        if initcheck:
            return jsonify({ "message" : "un-authorized" }), 401
        return jsonify({ "message" : "please re-login un-authorized ..." }), 401
@app.route("/refresh",methods=["POST"])
def validate_refresh():
    """_summary_

    Returns:
        _type_: _description_
    """
    payload = json.loads(request.data)
    token = payload["token"]
    public_id = ''
    try:
        jwt_decoded = jwt.decode(token, secret_key_refresh, algorithms=["HS256"])
        public_id = jwt_decoded["id"]
        datauser = {'public_id':jwt_decoded["id"]}
        token = createtoken(datauser)
        refresh = createrefreshtoken(datauser)
        check_key(dict_access,public_id,0)
        return jsonify({
                "token":token,
                "token_refresh":refresh
            }), 200
    except ZeroDivisionError:
        initcheck = False
        initcheck = check_key(dict_access,public_id,1)
        if initcheck:
            return jsonify({ "message" : "un-authorized" }), 401
        return jsonify({ "message" : "please re-login un-authorized ..." }), 401
def check_key(dictionary,public_id,typ = 0):
    """_summary_

    Args:
        dictionary (_type_): _description_
        public_id (_type_): _description_
        typ (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    if public_id in dictionary.keys():
        if dictionary.get(id) > 2 :
            print(dict_access.get(id))
            return False
        count = 0
        if typ == 0:
            count = 0
            dict.update({id:count})
            print(dict_access.get(id))
        elif typ > 0:
            x_count = dict_access.get(id)
            count = x_count+1
            dict.update({id:count})
            print(dict_access.get(id))
        return True
    count = 0
    dict_access[id] = count+1
    print(dict_access.get(id))
    return True
if __name__ == "__main__":
    JSONExceptionHandler(app)
    app.run(host=HOST, port=PORT)
    