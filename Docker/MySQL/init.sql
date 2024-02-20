
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
-- パスワードはdeleted_instructor
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