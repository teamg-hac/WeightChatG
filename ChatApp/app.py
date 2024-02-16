from flask import Flask, request, session, render_template, redirect, flash
import hashlib
import uuid
from datetime import datetime, timedelta, date
from models import dbConnect
import os
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import io
import base64
import re

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=7)

#登録画面の表示
@app.route('/signup')
def show_signup():
    is_instructor = request.args.get("is_instructor")
    return render_template('signup/signup.html', is_instructor=is_instructor)

#登録処理
@app.route('/signup',methods=['POST'])
def signup():
    user_name = request.form.get('user_name')
    mail = request.form.get('mail')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    is_instructor = request.form.get('is_instructor')
    latest_weight = request.form.get('latest_weight')
    height = request.form.get('height')
    goal = request.form.get('goal')
    introduction = request.form.get('introduction')
    address = request.form.get('address')
    icon_path  = request.form.get('image/*')

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
            UserId = str(u_id)
            session['uid'] = UserId
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
        users = dbConnect.getUserById(u_id) 
        return render_template('menu/mypage.html',users=users)
    
#体重記録の追加
@app.route('/add_record',methods=['POST'])
def add_record():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        record_room = dbConnect.getRecordRoom(u_id)
        record_room_id = record_room['record_room_id']
        value = request.form.get('weight') 
        created_at = datetime.now() 
        #created_at = datetime.strptime(created_at_str, '%Y-%m-%dT%H:%M')  # 文字列をdatetimeオブジェクトに変換
        dbConnect.addRecord(record_room_id, value, created_at)
        #dbConnect.updateweightById(record_room_id) エラーが出る。
        users = dbConnect.getUserById(u_id)
        return render_template('menu/mypage.html',users=users)

# トップ画面の表示
@app.route('/')
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
                return redirect('/index')
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
        return redirect('/')

# メニュー画面の表示
@app.route('/index')
def menu():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/')
    else:
        rooms = dbConnect.getRoomAll(u_id)
        user = dbConnect.getUserById(u_id)
        return render_template('menu/index.html', is_instructor=user['is_instructor'], rooms=rooms)

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
        password = request.form.get('password')
        height = request.form.get('height')
        height = float(height)
        goal = request.form.get('goal')
        introduction = request.form.get('introduction')
        address = request.form.get('address')
        is_instructor = request.form.get('is_instructor')
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
        if password == '':
            hash_password = user['password']
        else:
            hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        dbConnect.updateUser(u_id, user_name, mail, hash_password, is_instructor, height, goal, introduction, address, icon_path)
        # マイページができたら/mypageへリダイレクト
        return redirect('/edit-user')

# インストラクター一覧画面
@app.route('/instructors')
def instructors():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        instructors = dbConnect.getInstructors()
        rooms = dbConnect.getRoomAll(u_id)
        invited_u_ids = [x['invited_u_id'] for x in rooms]
        return render_template('menu/supporter.html', instructors=instructors, invited_u_ids=invited_u_ids)

# チャットルーム作成画面の表示
@app.route('/add-chatroom')
def show_add_chatroom():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        instructor_name = request.args.get('instructor_name')
        return render_template('menu/add_chatroom.html', instructor_name=instructor_name)

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
        return redirect('/index')

# チャットルームの削除
@app.route('/delete-room<int:room_id>')
def delete_room(room_id):
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        dbConnect.deleteChatRoom(room_id)
        return redirect('/index')
    

# 体重画面の表示
@app.route('/weight-page')
def weight_page():
    u_id = session.get('uid')
    if u_id is None:
        return redirect('/login')
    else:
        record_room_id = 1
        span = 'week'
        records = dbConnect.getRecordAll(record_room_id)
        room = dbConnect.getRecordRoomById(record_room_id)
        unit = room['unit']
        values = [float(x['value']) for x in records]
        dates = [y['created_at'].date() for y in records]
        if span == 'week':
            indicate = 7
        else:
            indicate = 30
            
        # day_of_week = dates[-1].weekday()
        indicate_values = values[-indicate:]
        indicate_dates = [a.strftime('%Y-%m-%d') for a in dates[-indicate:]]
        graph_dates = [z[-5:] for z in indicate_dates]
        plt.plot(graph_dates, indicate_values)
        
        # Y軸の目盛りを設定
        sample_value =round(round(indicate_values[-1], -1))
        scale = []
        for i in range(sample_value - 5, sample_value + 16, 5):
            scale.append(i)
        plt.yticks(scale)
        
        # Y軸のラベルを設定
        plt.ylabel(room['unit'])
        
        # グラフを画像として保存
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        
        # 画像をBase64にエンコード
        graph = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()
            
        return render_template('menu/weight_page.html', graph=graph, indicate=indicate, indicate_values=indicate_values, indicate_dates=indicate_dates, unit=unit)

# 404エラーの画面遷移
@app.errorhandler(404)
def error404(error):
    return render_template('error/404.html'),404

# 500エラーの画面遷移
@app.errorhandler(500)
def error404(error):
    return render_template('error/500.html'),500

if __name__ =='__main__':
    app.run(host="0.0.0.0", debug=True)