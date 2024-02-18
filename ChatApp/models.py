import pymysql
from flask import abort
from util.DB import DB


class dbConnect:
    # ユーザー情報の追加
    def createUser(u_id, user_name, mail, password, is_instructor, latest_weight, height, goal, introduction, address, icon_path):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO users (u_id, user_name, mail, password, is_instructor, latest_weight, height, goal, introduction, address, icon_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cur.execute(sql, (u_id, user_name, mail, password, is_instructor, latest_weight, height, goal, introduction, address, icon_path))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()
    
    # メールアドレスを指定してユーザー情報の取得
    def getUserByMail(mail):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE mail=%s;"
            cur.execute(sql, (mail))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()
    
    # ユーザー名を指定してユーザー情報の取得
    def getUserByName(user_name):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE user_name=%s;"
            cur.execute(sql, (user_name))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()
    
    # ユーザーIDを指定してユーザー情報の取得
    def getUserById(u_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE u_id=%s;"
            cur.execute(sql, (u_id))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()
            

    #追加　体重記録の追加に使用
    #ユーザーIDを指定して、usersテーブルの体重を更新する。
    def updateweightById(weight,u_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE users SET latest_weight = %s WHERE u_id= %s" 
            cur.execute(sql,(weight,u_id))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()      
        
    # すべてのインストラクター情報を取得
    def getInstructors():
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE is_instructor=1;"
            cur.execute(sql)
            instructors = cur.fetchall()
            return instructors
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()
    
    # 記録ルームの追加
    def addRecordRoom(record_name, u_id, unit, is_public, remind, remind_time):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO record_setting (record_name, u_id, unit, is_public, remind, remind_time) VALUES (%s, %s, %s, %s, %s, %s);"
            cur.execute(sql, (record_name, u_id, unit, is_public, remind, remind_time))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()
    
    # 記録ルームIDを指定してルーム情報を取得
    def getRecordRoomById(record_room_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM record_setting WHERE record_room_id=%s;"
            cur.execute(sql, (record_room_id))
            record_room = cur.fetchone()
            return record_room
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()
    
    # ユーザーIDを指定して記録ルーム情報をすべて取得
    def getRecordRoomAll(u_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM record_setting WHERE u_id=%s;"
            cur.execute(sql, (u_id))
            record_rooms = cur.fetchall()
            return record_rooms
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()
    # 追加
    # ユーザーIDを指定して記録ルーム情報を取得
    def getRecordRoom(u_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM record_setting WHERE u_id=%s;"
            cur.execute(sql, (u_id))
            record_rooms = cur.fetchone()
            return record_rooms
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()

    # 記録の追加
    def addRecord(record_room_id, value, created_at):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO records (record_room_id, value, created_at) VALUES (%s, %s, %s);"
            cur.execute(sql, (record_room_id, value, created_at))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()
    
    # 記録ルームIDを指定して該当ルームの持つ記録を取得
    def getRecordAll(record_room_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM records WHERE record_room_id=%s;"
            cur.execute(sql, (record_room_id))
            records = cur.fetchall()
            return records
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()
    
     #追加　体重記録の追加に使用
    #レコードルームIDを指定して、レコードテーブルの最新の情報を取得する。
    def getlatestrecordById(record_room_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM records WHERE record_room_id = %s ORDER BY created_at DESC LIMIT 1"
            cur.execute(sql,record_room_id,)
            latest_value = cur.fetchone()
            return latest_value
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()    
    
    
    #チャットルームの追加
    def addChatRoom(room_name, created_u_id, invited_u_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO rooms (room_name,created_u_id,invited_u_id) VALUES(%s, %s, %s);"
            cur.execute(sql,(room_name, created_u_id, invited_u_id))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()
    
    #チャットルームIDを指定してルーム情報を取得
    def getRoomByID(room_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM rooms WHERE room_id =%s;"
            cur.execute(sql,(room_id))
            room = cur.fetchone()
            return room
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
    
    #ユーザーIDを指定してチャットルーム情報をすべて取得
    def getRoomAll(u_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM rooms WHERE created_u_id = %s OR invited_u_id = %s;"
            cur.execute(sql,(u_id, u_id))
            rooms = cur.fetchall()
            return rooms
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            conn.close()
    # def getRoomAll(created_u_id):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = "SELECT * FROM rooms WHERE created_u_id =%s;"
    #         cur.execute(sql,(created_u_id))
    #         rooms = cur.fetchall()
    #         return rooms
    #     except Exception as e:
    #         print(str(e) + 'が発生しています')
    #         abort(500)
    #     finally:
    #         cur.close()
    
    # created_u_idとinvited_u_idを指定してチャットルーム情報を取得
    # 不要になったためコメントアウト
    # def getRoomByIDs(created_u_id, invited_u_id):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = "SELECT * FROM rooms WHERE created_u_id = %s AND invited_u_id = %s;"
    #         cur.execute(sql,(created_u_id, invited_u_id))
    #         room = cur.fetchone()
    #         return room
    #     except Exception as e:
    #         print(str(e) + 'が発生しています')
    #         abort(500)
    #     finally:
    #         cur.close()
    #         conn.close()

    #チャットルームIDを指定してルーム情報を削除
    def deleteChatRoom(room_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM rooms WHERE room_id =%s;"
            cur.execute(sql,(room_id))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    #メッセージの追加
    def addMessage(u_id, room_id, message, created_at):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages(u_id, room_id, message, created_at) VALUES(%s, %s, %s,%s);"
            cur.execute(sql,(u_id, room_id, message, created_at))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    #チャットルームIDを指定して該当チャンネルの持つメッセージを取得
    #修正　massageをmessageに修正
    def getMessageAll(room_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM messages WHERE room_id =%s;"
            cur.execute(sql,(room_id))
            messages = cur.fetchall()
            return messages
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()  

    #メッセージIDを指定してメッセージ情報を削除
    def deleteMessage(message_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE * FROM messages WHERE message_id =%s;"
            cur.execute(sql,(message_id))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()