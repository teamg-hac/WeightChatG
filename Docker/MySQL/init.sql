
DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users(
    u_id varchar(255) UNIQUE,
    user_name varchar(255) UNIQUE NOT NULL,
    mail varchar(255) UNIQUE NOT NULL,
    password varchar(255) NOT NULL,
    is_instructor int NOT NULL,
    latest_weight varchar(255),  
    height varchar(255),
    goal varchar(255),
    introduction varchar(255),
    address varchar(255),
    icon_path varchar(255) UNIQUE,
    PRIMARY KEY (u_id)
);

CREATE TABLE record_setting(
    record_room_id serial,
    record_name varchar(255) NOT NULL,
    u_id varchar(255) NOT NULL,
    unit varchar(255) NOT NULL,
    is_public int NOT NULL DEFAULT 0,
    remind int NOT NULL DEFAULT 0,
    remind_time time NOT NULL DEFAULT '00:00:00',
    PRIMARY KEY (record_room_id),
    FOREIGN KEY (u_id) REFERENCES users(u_id) ON DELETE CASCADE
);

CREATE TABLE records(
    record_id serial PRIMARY KEY,
    record_room_id bigint UNSIGNED NOT NULL,
    value varchar(255) NOT NULL,
    created_at timestamp NOT NULL,
    FOREIGN KEY (record_room_id) REFERENCES record_setting(record_room_id) ON DELETE CASCADE
);

CREATE TABLE rooms(
    room_id serial,
    room_name varchar(255) NOT NULL,
    created_u_id varchar(255) NOT NULL,
    invited_u_id varchar(255) NOT NULL,
    PRIMARY KEY (room_id),
    FOREIGN KEY (created_u_id) REFERENCES users(u_id) ON DELETE CASCADE,
    FOREIGN KEY (invited_u_id) REFERENCES users(u_id)
);

CREATE TABLE messages(
    message_id serial,
    room_id bigint UNSIGNED NOT NULL,
    u_id varchar(255) NOT NULL,
    message varchar(255) NOT NULL,
    created_at timestamp NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),
    FOREIGN KEY (u_id) REFERENCES users(u_id) ON DELETE CASCADE
);

-- 退会したインストラクター用アカウント
INSERT INTO users VALUES (
'f004a27b-c108-488e-bbff-970b30e0d437',
'deleted_instructor',
'deleted@sample.com',
'529c16bd76194a4b757597a652f4723266664795c3c287993c31adfa4955bd66',
1,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL);

-- テスト用
-- パスワード：hoge
INSERT INTO users VALUES (
'd7e35452-7550-4a3c-8a91-f256e6af1711',
'test',
'user1@sample.com',
'ecb666d778725ec97307044d642bf4d160aabb76f56c0069c71ea25b1e926825',
0,
60,
160,
'目指せ50㎏！',
'食べるのが大好きです',
'東京',
NULL);

INSERT INTO users VALUES ('6d0fc48d-2dc9-4ec6-b606-9a38987634af',
'hoge',
'user2@sample.com',
'08adcfea25123e115f37139697a4afd2948b262b27eee4ebe7d7d05317ce7360',
0,
120,
180,
'目指せ80㎏！',
'からあげ大好き',
'埼玉',
NULL);

-- パスワード：taro
INSERT INTO users VALUES ('854dd0b9-d172-4042-961d-cf7d9ccc0aee',
'太郎',
'instructor1@sample.com',
'8ff52c91ed7d509440aa7fbf04ad60ad554e4a01f101e5222916e70f9f68fb45',
1,
65,
175,
'ダイエットのお手伝い',
'走るの大好き',
'神奈川',
NULL);

-- パスワード：momoko
INSERT INTO users VALUES ('c21d4358-a010-46c2-853d-dc05cadae1d2',
'ももこ',
'instructor2@sample.com',
'41119377cc0303903198078cea7886b69dbbe87855e1f01d059dd2c4a1a1577d',
1,
50,
165,
'美しくなろう',
'エクササイズ大好き',
'大阪',
NULL);

INSERT INTO record_setting VALUES (1, '体重', 'd7e35452-7550-4a3c-8a91-f256e6af1711', 'kg', 0, 0, '00:00:00');

INSERT INTO records VALUES (1, 1, '70.0', '2024-01-01 15:30:00');
INSERT INTO records VALUES (2, 1, '69.8', '2024-01-02 15:30:00');
INSERT INTO records VALUES (3, 1, '69.0', '2024-01-03 15:30:00');
INSERT INTO records VALUES (4, 1, '68.0', '2024-01-04 15:30:00');
INSERT INTO records VALUES (5, 1, '67.0', '2024-01-05 15:30:00');
INSERT INTO records VALUES (6, 1, '66.0', '2024-01-06 15:30:00');
INSERT INTO records VALUES (7, 1, '67.0', '2024-01-07 15:30:00');
INSERT INTO records VALUES (8, 1, '68.0', '2024-01-08 15:30:00');
INSERT INTO records VALUES (9, 1, '68.0', '2024-01-09 15:30:00');
INSERT INTO records VALUES (10, 1, '68.0', '2024-01-10 15:30:00');
INSERT INTO records VALUES (11, 1, '67.0', '2024-01-11 15:30:00');
INSERT INTO records VALUES (12, 1, '68.0', '2024-01-12 15:30:00');
INSERT INTO records VALUES (13, 1, '67.0', '2024-01-13 15:30:00');
INSERT INTO records VALUES (14, 1, '66.8', '2024-01-14 15:30:00');
INSERT INTO records VALUES (15, 1, '66.0', '2024-01-15 15:30:00');
INSERT INTO records VALUES (16, 1, '67.0', '2024-01-16 15:30:00');
INSERT INTO records VALUES (17, 1, '67.2', '2024-01-17 15:30:00');
INSERT INTO records VALUES (18, 1, '67.0', '2024-01-18 15:30:00');
INSERT INTO records VALUES (19, 1, '67.0', '2024-01-19 15:30:00');
INSERT INTO records VALUES (20, 1, '67.0', '2024-01-20 15:30:00');
INSERT INTO records VALUES (21, 1, '67.0', '2024-01-21 15:30:00');
INSERT INTO records VALUES (22, 1, '66.8', '2024-01-22 15:30:00');
INSERT INTO records VALUES (23, 1, '66.6', '2024-01-23 15:30:00');
INSERT INTO records VALUES (24, 1, '66.3', '2024-01-24 15:30:00');
INSERT INTO records VALUES (25, 1, '66.0', '2024-01-25 15:30:00');
INSERT INTO records VALUES (26, 1, '66.0', '2024-01-26 15:30:00');
INSERT INTO records VALUES (27, 1, '66.0', '2024-01-27 15:30:00');
INSERT INTO records VALUES (28, 1, '65.8', '2024-01-28 15:30:00');
INSERT INTO records VALUES (29, 1, '65.8', '2024-01-29 15:30:00');
INSERT INTO records VALUES (30, 1, '65.8', '2024-01-30 15:30:00');
INSERT INTO records VALUES (31, 1, '65.0', '2024-01-31 15:30:00');