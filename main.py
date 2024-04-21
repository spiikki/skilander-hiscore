# Skilander HiScore API
# 2024 hemohespiikki of hiihtoliitto

from datetime import datetime
from flask import Flask, jsonify, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

@app.get("/")
def root():
    return "vote for seppo!"

@app.route("/<level>", methods=["GET"])
def get_scores(level):
    sql_read = ''' SELECT user_id,time,collectibles,player FROM scores WHERE level=? ORDER BY time ASC LIMIT 10'''
    db_conn = do_db_con()
    db_cur = db_conn.cursor()
    db_cur.execute(sql_read, level)
    rows = db_cur.fetchall()
    db_conn.close()
    return rows

@app.route("/all", methods=["GET"])
def get_all_scores():
    sql_read = ''' SELECT user_id,time,collectibles,player FROM scores WHERE level=? ORDER BY level DESC, time ASC LIMIT 10'''
    db_conn = do_db_con()
    db_cur = db_conn.cursor()
    result = []
    for level in range(0,5):
        db_cur.execute(sql_read, str(level))
        result.append(db_cur.fetchall())
    db_conn.close()
    return result


@app.route("/<level>/submit", methods=["POST"])
def save_score(level):
    sql_save = ''' INSERT INTO scores (user_id, level, player, collectibles, time, timestamp) VALUES (?,?,?,?,?,?) '''
    data = request.get_json()
    db_conn = do_db_con()
    db_cur = db_conn.cursor()
    db_cur.execute(sql_save, (data[0], level, data[3], data[2], data[1], datetime.now()))
    db_conn.commit()
    db_conn.close()
    return data

@app.route("/<user_id>/hiscores", methods=["POST"])
def save_hiscore(user_id):
    pass

def do_db_con():
    try:
        db_conn = sqlite3.connect(r"./database/ski.db")
        return db_conn
    except Error as e:
        print(e)

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0",port=80)