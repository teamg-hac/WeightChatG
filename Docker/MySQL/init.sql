
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
    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE CASCADE,
    FOREIGN KEY (u_id) REFERENCES users(u_id) ON DELETE CASCADE
);

-- 退会したインストラクター用アカウント
INSERT INTO users VALUES (
    'f004a27b-c108-488e-bbff-970b30e0d437',
    'deleted_instructor',
    'deleted@sample.com','529c16bd76194a4b757597a652f4723266664795c3c287993c31adfa4955bd66',
    1,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL);


-- テストユーザー
-- パスワード：taro
INSERT INTO users VALUES (
    '854dd0b9-d172-4042-961d-cf7d9ccc0aee',
    '太郎',
    'testuser@sample.com',
    '8ff52c91ed7d509440aa7fbf04ad60ad554e4a01f101e5222916e70f9f68fb45',
    0,
    NULL,
    175,
    '今年中に60kgを達成する',
    'おいしいものが大好き',
    '東京',
    NULL);

INSERT INTO record_setting VALUES (
    1,
    '体重',
    '854dd0b9-d172-4042-961d-cf7d9ccc0aee',
    'kg',
    0,
    0,
    '00:00:00');

INSERT INTO records VALUES (1, 1, '70.0', '2024-02-01 15:30:00');
INSERT INTO records VALUES (2, 1, '69.8', '2024-02-02 15:30:00');
INSERT INTO records VALUES (3, 1, '69.0', '2024-02-03 15:30:00');
INSERT INTO records VALUES (4, 1, '68.0', '2024-02-04 15:30:00');
INSERT INTO records VALUES (5, 1, '67.0', '2024-02-05 15:30:00');
INSERT INTO records VALUES (6, 1, '66.0', '2024-02-06 15:30:00');
INSERT INTO records VALUES (7, 1, '67.0', '2024-02-07 15:30:00');
INSERT INTO records VALUES (8, 1, '68.0', '2024-02-08 15:30:00');
INSERT INTO records VALUES (9, 1, '68.0', '2024-02-09 15:30:00');
INSERT INTO records VALUES (10, 1, '68.0', '2024-02-10 15:30:00');
INSERT INTO records VALUES (11, 1, '67.0', '2024-02-11 15:30:00');
INSERT INTO records VALUES (12, 1, '68.0', '2024-02-12 15:30:00');
INSERT INTO records VALUES (13, 1, '67.0', '2024-02-13 15:30:00');
INSERT INTO records VALUES (14, 1, '66.8', '2024-02-14 15:30:00');
INSERT INTO records VALUES (15, 1, '66.0', '2024-02-15 15:30:00');
INSERT INTO records VALUES (16, 1, '67.0', '2024-02-16 15:30:00');
INSERT INTO records VALUES (17, 1, '67.2', '2024-02-17 15:30:00');
INSERT INTO records VALUES (18, 1, '67.0', '2024-02-18 15:30:00');
INSERT INTO records VALUES (19, 1, '67.0', '2024-02-19 15:30:00');
INSERT INTO records VALUES (20, 1, '67.0', '2024-02-20 15:30:00');
INSERT INTO records VALUES (21, 1, '67.0', '2024-02-21 15:30:00');
INSERT INTO records VALUES (22, 1, '66.8', '2024-02-22 15:30:00');
INSERT INTO records VALUES (23, 1, '66.6', '2024-02-23 15:30:00');
INSERT INTO records VALUES (24, 1, '66.3', '2024-02-24 15:30:00');
INSERT INTO records VALUES (25, 1, '66.0', '2024-02-25 15:30:00');
INSERT INTO records VALUES (26, 1, '66.0', '2024-02-26 15:30:00');
INSERT INTO records VALUES (27, 1, '66.0', '2024-02-27 15:30:00');
INSERT INTO records VALUES (28, 1, '65.8', '2024-02-28 15:30:00');
INSERT INTO records VALUES (29, 1, '65.8', '2024-02-29 15:30:00');