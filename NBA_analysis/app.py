# _*_ coding: utf-8 _*_
import json
import sqlite3
import pandas as pd
from flask import Flask, render_template, jsonify
from statsmodels.tsa.arima.model import ARIMA

app = Flask(__name__)
app.debug = True

login_name = None

all_players = []
with open('nab_player.json', 'r', encoding='utf8') as f:
    for line in f:
        player = json.loads(line.strip())

        info = {
            '姓名': player['playerProfile']['displayName'],
            '赛季': player['season'],
            "排名": player['rank'],
            "球队": player['teamProfile']['name'],
            "场数": player['statAverage']['games'],
            "先发": player['statAverage']['gamesStarted'],
            "场均得分": player['statAverage']['pointsPg'],
            "场均篮板": player['statAverage']['rebsPg'],
            "场均助攻": player['statAverage']['assistsPg'],
            "分钟": player['statAverage']['minsPg'],
            "效率": player['statAverage']['fgpct'],
            "三分": player['statAverage']['tppct'],
            "罚球": player['statAverage']['ftpct'],
            "进攻": player['statAverage']['offRebsPg'],
            "防守": player['statAverage']['defRebsPg'],
            "场均抢断": player['statAverage']['stealsPg'],
            "场均盖帽": player['statAverage']['blocksPg'],
            "失误": player['statAverage']['turnoversPg'],
            "犯规": player['statAverage']['foulsPg']
        }
        all_players.append(info)

all_players = pd.DataFrame(all_players, )
print(all_players)


# --------------------- html render ---------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/player_basic_analysis')
def player_basic_analysis():
    return render_template('player_basic_analysis.html')


@app.route('/player_predict')
def player_predict():
    return render_template('player_predict.html')


# ------------------ ajax restful api -------------------
@app.route('/check_login')
def check_login():
    """判断用户是否登录"""
    return jsonify({'username': login_name, 'login': login_name is not None})


@app.route('/register/<name>/<password>')          # 注册功能
def register(name, password):
    conn = sqlite3.connect('user_info.db')     # 打开user_info.db数据库文件
    cursor = conn.cursor()      # 获取游标

    check_sql = "SELECT * FROM sqlite_master where type='table' and name='user'"     # check_sql语句 查看指定名为user的表的信息
    cursor.execute(check_sql)      # 执行check_sql语句
    results = cursor.fetchall()     # 接收返回值
    # 数据库表不存在
    if len(results) == 0:
        # 创建数据库表
        sql = """
                CREATE TABLE user(
                    name CHAR(256), 
                    password CHAR(256)
                );
                """
        cursor.execute(sql)
        conn.commit()     # 提交数据库操作
        print('创建数据库表成功！')

    sql = "INSERT INTO user (name, password) VALUES (?,?);"    # sql语句 在user表中name列和password列插入数据
    cursor.executemany(sql, [(name, password)])     # 批量执行sql语句
    conn.commit()
    return jsonify({'info': '用户注册成功！', 'status': 'ok'})


@app.route('/login/<name>/<password>')       # 登录功能
def login(name, password):
    global login_name
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()

    check_sql = "SELECT * FROM sqlite_master where type='table' and name='user'"
    cursor.execute(check_sql)
    results = cursor.fetchall()
    # 数据库表不存在
    if len(results) == 0:
        # 创建数据库表
        sql = """
                CREATE TABLE user(
                    name CHAR(256), 
                    password CHAR(256)
                );
                """
        cursor.execute(sql)
        conn.commit()
        print('创建数据库表成功！')

    sql = "select * from user where name='{}' and password='{}'".format(name, password)
    cursor.execute(sql)
    results = cursor.fetchall()

    login_name = name
    if len(results) > 0:
        return jsonify({'info': name + '用户登录成功！', 'status': 'ok'})
    else:
        return jsonify({'info': '当前用户不存在！', 'status': 'error'})


@app.route('/get_all_players')
def get_all_players():
    """获取所有球员名称"""
    dis_count = all_players['姓名'].value_counts()
    print(len(dis_count))
    return jsonify(list(dis_count.keys()))


@app.route('/player_statistic/<player>')
def player_statistic(player):
    df = all_players[all_players['姓名'] == player]

    return jsonify({
        '赛季': df['赛季'].values.tolist(),
        '场均得分': df['场均得分'].values.tolist(),
        '场数': df['场数'].values.tolist(),

        "场均篮板": df['场均篮板'].values.tolist(),
        "场均助攻": df['场均助攻'].values.tolist(),
        "场均抢断": df['场均抢断'].values.tolist(),
        "场均盖帽": df['场均盖帽'].values.tolist(),

        "分钟": df['分钟'].values.tolist(),
        "效率": df['效率'].values.tolist(),

        "三分": df['三分'].values.tolist(),
        "罚球": df['罚球'].values.tolist(),
        "进攻": df['进攻'].values.tolist(),
        "防守": df['防守'].values.tolist(),
    })


def arima_model_train_eval(history):
    # 构造 ARIMA 模型
    model = ARIMA(history, order=(1, 1, 0))
    # 基于历史数据训练
    model_fit = model.fit()
    # 预测下一个时间步的值
    output = model_fit.forecast()
    yhat = output[0]
    return yhat


@app.route('/future_predict/<player>')
def future_predict(player):
    df = all_players[all_players['姓名'] == player]
    # 赛季
    saijis = df['赛季'].values.tolist()
    saijis.append('2022')

    # 场均得分
    scores = df['场均得分'].values.tolist()
    predict_score = arima_model_train_eval(scores)
    scores.append(predict_score)

    # 场均篮板
    lanbans = df['场均篮板'].values.tolist()
    predict_lanban = arima_model_train_eval(lanbans)
    lanbans.append(predict_lanban)

    # 场均助攻
    zhugongs = df['场均助攻'].values.tolist()
    predict_zhugong = arima_model_train_eval(zhugongs)
    zhugongs.append(predict_zhugong)

    # 场均抢断
    qiangduans = df['场均抢断'].values.tolist()
    predict_qiangduan = arima_model_train_eval(qiangduans)
    qiangduans.append(predict_qiangduan)

    return jsonify({
        '赛季': saijis,
        '场均得分': scores,
        '场均篮板': lanbans,
        '场均助攻': zhugongs,
        '场均抢断': qiangduans,
    })

if __name__ == "__main__":
    app.run(host='127.0.0.1')
