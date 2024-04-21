# Skilander HiScore API
# 2024 hemohespiikki of hiihtoliitto

from datetime import datetime
from flask import Flask, jsonify, request
import hashlib
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

@app.get("/")
def root():
    return "vote for seppo!"

@app.route("/<level>", methods=["GET"])
def get_scores(level):
    sql_read = ''' SELECT time,collectibles,player FROM scores WHERE level=? ORDER BY time ASC LIMIT 10'''
    db_conn = do_db_con()
    db_cur = db_conn.cursor()
    db_cur.execute(sql_read, level)
    rows = db_cur.fetchall()
    db_conn.close()
    return rows

@app.route("/all", methods=["GET"])
def get_all_scores():
    sql_read = ''' SELECT time,collectibles,player FROM scores WHERE level=? ORDER BY level DESC, time ASC LIMIT 10'''
    db_conn = do_db_con()
    db_cur = db_conn.cursor()
    result = []
    for level in range(0,5):
        db_cur.execute(sql_read, str(level))
        result.append(db_cur.fetchall())
    db_conn.close()
    return result

@app.route("/<level>/submit/<user_id>", methods=["POST"])
def save_score(level, user_id):
    sql_save = ''' INSERT INTO scores (user_id, level, player, collectibles, time, timestamp) VALUES (?,?,?,?,?) '''
    data = request.get_json()
    db_conn = do_db_con()
    db_cur = db_conn.cursor()
    db_cur.execute(sql_save, (user_id, level, data[2], data[1], data[0], datetime.now()))
    db_conn.commit()
    db_conn.close()
    return data

@app.route("/user", methods=["POST"])
def user():
    sql_find = ''' SELECT id, password, initials FROM users WHERE username='''
    sql_save = ''' INSERT INTO users (id, username, password, initials, timestamp) VALUES (?,?,?,?,?) '''
    sql_latest_uid = ''' SELECT id, timestamp FROM users ORDER BY 2 DESC LIMIT 1 '''
    data = request.get_json()
    app.logger.debug(data["username"])
    db_conn = do_db_con()
    db_cur = db_conn.cursor()

    db_cur.execute(sql_find+"\""+data["username"]+"\"")

    user_data = db_cur.fetchall()
    app.logger.debug(user_data)
    app.logger.debug(len(user_data))
    if len(user_data) == 1:
        if user_data[0][1] == data["password"]:
            app.logger.debug("user found!")
            result = {
                "user_id": user_data[0][0],
                "initials": user_data[0][2]
            }
        else:
            app.logger.debug("wrong pwd")
            result = "baby don't hack me, no more!"
    else:
        app.logger.debug("new user")
        db_cur.execute(sql_latest_uid)
        latest = db_cur.fetchone()
        seed=latest[0]+data["username"]
        id=hashlib.md5(seed.encode("utf_8")).hexdigest()
        db_cur.execute(sql_save, (id, data["username"], data["password"], data["initials"], datetime.now()))
        db_conn.commit()
        result = {
            "user_id": id,
            "initials": data["initials"]
        }

    db_conn.close()
    return result


def do_db_con():
    try:
        db_conn = sqlite3.connect(r"./database/ski.db")
        return db_conn
    except Error as e:
        print(e)

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0",port=80)