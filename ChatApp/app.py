from flask import Flask, request, session, render_template, redirect, flash, url_for
import hashlib
import uuid
from datetime import datetime, timedelta, timezone, date
from models import dbConnect
import os
from werkzeug.utils import secure_filename
import unicodedata
import matplotlib.pyplot as plt
import io
import base64
import re
from flask_paginate import Pagination, get_page_parameter
import pandas as pd
import calendar
import math

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=7)

#登録画面の表示
@app.route('/signup')
def show_signup():
    return render_template('signup/signup.html')

#登録処理
@app.route('/signup', methods=['POST'])
def signup():
    user_name = request.form.get('user_name')
    mail = request.form.get('mail')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    is_instructor = request.form.get('is_instructor')
    latest_weight = request.form.get('latest_weight')
    height = request.form.get('height')
    if latest_weight == '' or latest_weight is None:
        latest_weight = None
    else:
        latest_weight = float(latest_weight)

    if height == '' or height is None:
        height = None
    else:
        height = float(height)
    goal = request.form.get('goal', None)
    introduction = request.form.get('introduction', None)
    address = request.form.get('address', None)
    icon_path  = request.files.get('icon', None)
    
    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if user_name == '' or mail =='' or password1 == '' or password2 == '':
        flash('空のフォームがあるようです')
    elif password1 != password2:
        flash('二つのパスワードの値が違っています')
    elif re.match(pattern, mail) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        u_id = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        DBuser_mail = dbConnect.getUserByMail(mail)
        DBuser_name = dbConnect.getUserByName(user_name)

        if DBuser_mail != None:
            flash('メールアドレスは既に登録されているようです')
        elif DBuser_name != None:
            flash('ユーザー名は既に登録されているようです')
        else:
            dbConnect.createUser(u_id, user_name, mail, password, is_instructor, latest_weight, height, goal, introduction, address, icon_path)
            record_name= '体重'
            unit= 'kg'
            is_public = 0
            remind = 0 
            remind_time = "00:00:00"
            dbConnect.addRecordRoom(record_name, u_id, unit, is_public, remind, remind_time)
            return redirect('/login')
    return redirect('/signup')

#マイページ画面の表示
@app.route('/mypage')
def show_mypage():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        user = dbConnect.getUserById(u_id)
        weight_record = dbConnect.getWeightRecordById(u_id)
        latest_record = dbConnect.getLatestRecordById(weight_record['record_room_id'])
        if latest_record:
            latest_record_timestamp = str(latest_record['created_at'])
        else:
            latest_record_timestamp = None
        return render_template('menu/mypage.html',user=user, latest_record_timestamp=latest_record_timestamp)
    
#体重記録の追加
@app.route('/add-record', methods=['POST'])
def add_record():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        # record_room = dbConnect.getRecordRoom(u_id)
        record_room = dbConnect.getWeightRecordById(u_id)
        record_room_id = record_room['record_room_id']
        value = request.form.get('weight')
        # 全角の数字を半角に変換
        value = unicodedata.normalize('NFKC', value)
        # valueが数値の文字列か判定
        try:
            result = float(value)
        except ValueError:
            flash('数値を入力してください')
            return redirect('/mypage')
        
        created_at = datetime.now(timezone(timedelta(hours=9)))
        
        # 最新の記録の日にちを確認し、同じであれば上書きをするか確認
        # latest_record = dbConnect.getLatestRecordById(record_room_id)
        # if str(latest_record['created_at'])[:11] == str(created_at)[:11]:
        #     flash('今日は記録済みです。上書きしますか？')
        #     return redirect()
        
        dbConnect.addRecord(record_room_id, value, created_at)
        # value = dbConnect.getlatestrecordById(record_room_id)
        # weight = value['value']
        # weight = float(weight)
        dbConnect.updateweightById(value, u_id)
        #users = dbConnect.getUserById(u_id)
        return redirect('/mypage')

#チャット表示
@app.route('/room<int:room_id>', methods=['GET'])
def show_messages(room_id):
    u_id = session.get("uid")
    if u_id is None:
        return redirect('/login')
    else:
        user = dbConnect.getUserById(u_id) 
        messages = dbConnect.getMessageAll(room_id)
        room = dbConnect.getRoomByID(room_id)
        
        if user['is_instructor'] == 0:
            chat_u_id = room['invited_u_id']
            is_public = None
        else:
            chat_u_id = room['created_u_id']
            weight_record = dbConnect.getWeightRecordById(chat_u_id)
            is_public = weight_record['is_public']
        
        chat_user = dbConnect.getUserById(chat_u_id)
        
        return render_template('chat/chat.html',room=room, user=user, messages=messages, chat_user=chat_user, is_public=is_public)
    
#チャット投稿
@app.route('/add-message',methods=['POST'])
def add_message():
    u_id = session.get("uid")
    if u_id is None:
        return redirect('/login')
    else:
        room_id = request.form.get('room_id')
        message  = request.form.get('message')
        created_at = datetime.now()

    if message:
        dbConnect.addMessage(u_id, room_id, message, created_at)
    return redirect('/room{room_id}'.format(room_id=room_id))

# トップ画面の表示
@app.route('/index')
def top():
    return render_template('top.html')

# ログイン画面の表示
@app.route('/login')
def show_login():
    return render_template('login/user_login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def login():
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    if mail == '' and password == '':
        flash('メールアドレスとパスワードを入力してください')
    elif mail == '':
        flash('メールアドレスを入力してください')
    elif password == '':
        flash('パスワードを入力してください')
    else:
        user = dbConnect.getUserByMail(mail)
        if user is None:
            flash('このメールアドレスは登録されていません')
        else:
            hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hash_password != user['password']:
                flash('パスワードが違います')
            else:
                session['uid'] = user['u_id']
                return redirect('/')
    return redirect('/login')

# ログアウト処理
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# 退会処理
@app.route('/delete-user', methods=['POST'])
def delete_user():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        user = dbConnect.getUserById(u_id)
        if user['is_instructor'] == 1:
            instructor = dbConnect.getUserByName('deleted_instructor')
            dbConnect.updateRoomByInvited(instructor['u_id'], user['u_id'])
        session.clear()
        dbConnect.deleteUser(u_id)
        flash('退会しました')
        return redirect('/index')

# メニュー画面の表示
@app.route('/')
def menu():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/index')
    
    rooms = dbConnect.getRoomAll(u_id)
    user = dbConnect.getUserById(u_id)
    
    # チャット相手のユーザー名リスト（users_name）を作成
    if user['is_instructor'] == 0:
        chat_u_id = [x['invited_u_id'] for x in rooms]
    else:
        chat_u_id = [x['created_u_id'] for x in rooms]
    users_name = []
    for i in chat_u_id:
        users_name.append(dbConnect.getUserById(i)['user_name'])
    
    # 各チャットルームの最新投稿がユーザーかどうか判定するためのリストを作成
    room_ids = [x['room_id'] for x in rooms]
    latest_u_ids = []
    for j in room_ids:
        latest_u_id = dbConnect.getLatestMessageUidByRoomId(j)
        if latest_u_id:
            latest_u_ids.append(latest_u_id['u_id'])
        latest_u_ids.append('')
        
    
    return render_template('index.html', user=user, rooms=rooms, users_name=users_name, latest_u_ids=latest_u_ids)


# ユーザー情報の編集画面表示
@app.route('/edit-user')
def show_edit_user():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        user = dbConnect.getUserById(u_id)
        return render_template('menu/edit_user.html', user=user)

# ユーザー情報の編集処理
@app.route('/edit-user', methods=['POST'])
def edit_user():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        file = request.files.get('icon')
        user_name = request.form.get('user_name')
        mail = request.form.get('mail')
        height = request.form.get('height')
        goal = request.form.get('goal')
        introduction = request.form.get('introduction')
        address = request.form.get('address')
        # is_instructor = request.form.get('is_instructor')
        user = dbConnect.getUserById(u_id)
        icon_name = secure_filename(file.filename)
        # 新しい画像ファイルを受取ったか確認
        if icon_name == '':
            icon_path = user['icon_path']
        else:
            # 同名のファイルの有無をチェック
            icon_path = os.path.join('static/img_add', icon_name)
            icon_paths = dbConnect.getIconPath()
            if icon_path in icon_paths:
                flash('画像のファイル名を変更してください')
                return redirect('/edit-user')
            # 古い画像ファイルの削除
            if user['icon_path'] is not None:
                os.remove(user['icon_path'])
            # 受取った写真（icon）をimg_addフォルダに保存
            file.save(icon_path)
        
        # 新しいpasswordを受取ったか確認
        # if password == ''
            # hash_password = user['password']
        # else:
            # hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        dbConnect.updateUser(u_id, user_name, mail, height, goal, introduction, address, icon_path)
        return redirect('/mypage')

# インストラクター一覧画面
@app.route('/instructors')
def instructors():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        instructors = dbConnect.getInstructors()
        rooms = dbConnect.getRoomAll(u_id)
        user = dbConnect.getUserById(u_id)
        invited_u_ids = [x['invited_u_id'] for x in rooms]
        return render_template('menu/supporter.html', instructors=instructors, user=user, invited_u_ids=invited_u_ids)

# チャットルーム作成画面の表示
@app.route('/add-chatroom')
def show_add_chatroom():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        instructor_name = request.args.get('instructor_name')
        user = dbConnect.getUserById(u_id)
        return render_template('menu/add_chatroom.html', instructor_name=instructor_name, user=user)

# チャットルームの作成処理
@app.route('/add-chatroom', methods=['POST'])
def add_chatroom():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        instructor_name = request.form.get('instructor_name')
        room_name = request.form.get('room_name')
        instructor = dbConnect.getUserByName(instructor_name)
        instructor_id = instructor['u_id']
        dbConnect.addChatRoom(room_name, u_id, instructor_id)
        return redirect('/')

# チャットルームの削除
@app.route('/delete-room<int:room_id>', methods=['POST'])
def delete_room(room_id):
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        dbConnect.deleteChatRoom(room_id)
        return redirect('/')
    

# 体重画面の表示
@app.route('/weight-page')
def weight_page():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    
    user = dbConnect.getUserById(u_id)
    record_room = dbConnect.getWeightRecordById(u_id)
    record_room_id = record_room['record_room_id']
    unit = record_room['unit']
    span = request.args.get('span')
    get_records = dbConnect.getRecordAll(record_room_id)
    # データが日付順に並んでいない場合を考慮して並べ替え
    records = sorted(get_records, key=lambda x: x['created_at'])
    
    # まだ記録が無い場合はマイページにリダイレクト
    if not records:
        flash('まだ記録がありません')
        return redirect('/mypage')
    
    # 表示する範囲の日にちの入ったリスト(正確にはリストじゃない)を作成
    latest_year = records[-1]['created_at'].year
    latest_month = records[-1]['created_at'].month
    latest_day = records[-1]['created_at'].day
    oldest_year = records[0]['created_at'].year
    oldest_month = records[0]['created_at'].month
    oldest_day = records[0]['created_at'].day
    start = datetime.strptime(str(oldest_year) + '-' + str(oldest_month) + '-' + str(oldest_day), '%Y-%m-%d')
    end = datetime.strptime(str(latest_year) + '-' + str(latest_month) + '-' + str(latest_day), '%Y-%m-%d')
    indicate_dates = pd.date_range(start, end)
    indicate_dates = [str(y)[:16] for y in indicate_dates]
    
    # 指定した範囲の日付のうち、記録があれば日時と記録を追加
    # 記録が無ければNoneを追加
    dates = []
    values = []
    ids = []
    for i in indicate_dates:
        for j in records:
            if i[:10] == str(j['created_at'])[:10]:
                dates.append(str(j['created_at'])[:16].replace('-', '/'))
                values.append(float(j['value']))
                ids.append(j['record_id'])
                break
        else:
            dates.append(i.replace('-', '/'))
            values.append(None)
            ids.append(None)
    
    
    # リストのページネーション
    page_list = request.args.get(get_page_parameter('list'), type=int, default=1)
    
    count = 0
    # if latest_month + 1 - page_list <= 0:
    if latest_month + 1 - page_list == 0:
        count += 1
    elif latest_month + 1 - page_list == -12:
        count += 2
    elif latest_month + 1 - page_list == -24:
        count += 3
    elif latest_month + 1 - page_list == -36:
        count += 4
    elif latest_month + 1 - page_list == -48:
        count += 5
    year = latest_year - count
    month = latest_month + 1 - page_list + (12 * count)
    per_page_list = calendar.monthrange(year, month)[1]
    
    if len(str(month)) == 1:
        month = '0' + str(month)
    
    # 日付だけのリストを作成
    no_times = [c[:10] for c in dates]
    if str(year) + '/' + month + '/01' in no_times:
        start_list = no_times.index(str(year) + '/' + month + '/01')
    else:
        start_list = 0
    if str(year) + '/' + month + '/' + str(per_page_list) in no_times:
        end_list = no_times.index(str(year) + '/' + month + '/' + str(per_page_list))
    else:
        end_list = None
    
    if end_list:
        list_values = values[start_list:end_list + 1]
        list_dates = dates[start_list:end_list + 1]
        list_ids = ids[start_list:end_list + 1]
    else:
        list_values = values[start_list:]
        list_dates = dates[start_list:]
        list_ids = ids[start_list:]
    
    pagination_list = Pagination(list=page_list, per_page=per_page_list, total=len(indicate_dates), prev_label='次へ', next_label='前へ', page_parameter='list')
    
    
    # グラフのページネーション
    if span == 'week':
        per_page = 7
    elif span == 'month':
        per_page = 30
    elif span == 'year':
        per_page = 365
    else:
        per_page = 7
    
    page_graph = request.args.get(get_page_parameter('graph'), type=int, default=1)
    
    pagination_graph = Pagination(graph=page_graph, per_page=per_page, total=len(indicate_dates), prev_label='次へ', next_label='前へ', page_parameter='graph')        
    
    # 表示する範囲
    start_graph = (page_graph - 1) * per_page
    end_graph = page_graph * per_page
    values.reverse()
    graph_values = values[start_graph:end_graph]
    graph_values.reverse()
    dates.reverse()
    graph_dates = dates[start_graph:end_graph]
    graph_dates = [a[:10] for a in graph_dates]
    graph_dates.reverse()
    
    fig, ax = plt.subplots()
    plt.plot(graph_dates, graph_values, marker="o")
    
    # X軸の目盛りを設定
    fig.autofmt_xdate(ha='center')
    
    # Y軸の目盛りを設定
    y_values = [float(x['value']) for x in records]
    max_value = round(max(y_values)) + 5
    min_value = round(min(y_values)) - 5
    scale = []
    while min_value <= max_value:
        scale.append(min_value)
        min_value += 2
    plt.yticks(scale)
    
    # Y軸のラベルを設定
    plt.ylabel(unit)
    
    # グラフを画像として保存
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # 画像をBase64にエンコード
    graph = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
            
    return render_template('menu/weight_page.html', graph=graph, list_values=list_values, list_dates=list_dates, list_ids=list_ids, unit=unit, user=user, pagination_list=pagination_list, pagination_graph=pagination_graph)

    
# 記録した体重の削除
@app.route('/delete-value', methods=['POST'])
def delete_value():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    
    record_id = request.form.get('record_id')
    
    record = dbConnect.getRecordById(record_id)
    record_room_id = record['record_room_id']
    latest_record = dbConnect.getLatestRecordById(record_room_id)
    
    # 体重記録の削除
    if record_id:
        dbConnect.deleteValueById(record_id)
    
    # 削除した記録が最新だった場合、usersのlatest_weightを更新
    if int(record_id) == latest_record['record_id']:
        new_latest_record = dbConnect.getLatestRecordById(record_room_id)
        new_value = new_latest_record['value']
        dbConnect.updateweightById(new_value, u_id)

    return redirect('/weight-page')


# 記録ルーム追加画面の表示
@app.route('/add-recordroom')
def show_add_recordroom():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        return render_template('option/add_recordroom.html')
        
# 記録ルーム作成処理
@app.route('/add-recordroom', methods=['POST'])
def add_recordroom():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        record_name = request.form.get('record_name')
        unit = request.form.get('unit')
        is_public = request.form.get('is_public')
        remind = request.form.get('remind')
        remind_time = request.form.get('remind_time')
        if record_name == '':
            flash('記録名を入力してください')
        elif unit == '':
            flash('単位を入力してください')
        else:
            if remind_time == '':
                remind_time = '00:00:00'
            dbConnect.addRecordRoom(record_name, u_id, unit, is_public, remind, remind_time)
            return redirect('/mypage')
        return redirect('/add-recordroom')

# 記録ルーム情報の更新画面表示
@app.route('/edit-recordroom<record_room_id>')
def show_edit_recordroom(record_room_id):
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        record_room = dbConnect.getRecordRoomById(record_room_id)
        return render_template('option/edit_recordroom.html', record_room=record_room)

# 記録ルーム情報の更新
@app.route('/edit-recordroom<record_room_id>', methods=['POST'])
def edit_recordroom(record_room_id):
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        record_name = request.form.get('record_name')
        unit = request.form.get('unit')
        is_public = request.form.get('is_public')
        remind = request.form.get('remind')
        remind_time = request.form.get('remind_time')
        dbConnect.updateRecordRoom(record_room_id, record_name, unit, is_public, remind, remind_time)
        return redirect('/mypage')

# 404エラーの画面遷移
@app.errorhandler(404)
def error404(error):
    return render_template('error/404.html'),404

# 500エラーの画面遷移
@app.errorhandler(500)
def error500(error):
    return render_template('error/500.html'),500

if __name__ =='__main__':
    app.run(host="0.0.0.0", debug=True)