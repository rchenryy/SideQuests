use squest_db;

DROP TABLE IF EXISTS rsvp;
DROP TABLE IF EXISTS response;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS user;


CREATE TABLE user(
    uid int AUTO_INCREMENT PRIMARY KEY,
    name varchar(30) NOT NULL,
    class int NOT NULL,
    dio varchar(250),
    dob date NOT NULL,
    email char(5) NOT NULL,
    password varchar(255) NOT NULL 
)

CREATE TABLE event(
    uid int,
    eid int AUTO_INCREMENT PRIMARY KEY,
    event_name varchar(30) NOT NULL,
    event_type set('food', 'academic', 'nightlife', 
    'music', 'cultural', 'sport', 'nature', 'other') NOT NULL,
    city varchar(30) NOT NULL,
    date datetime NOT NULL,
    meeting_point varchar(100) NOT NULL,
    description varchar(500) NOT NULL,
    attachment varchar(500),
    price float NOT NULL
)

CREATE TABLE comment(
    uid int,
    eid int,
    cid int AUTO_INCREMENT PRIMARY KEY,
    comment varchar(250) NOT NULL
)

CREATE TABLE response(
    uid int,
    eid int,
    cid int,
    rid int AUTO_INCREMENT PRIMARY KEY,
    response varchar(250) NOT NULL
)

CREATE TABLE rsvp(
    uid int PRIMARY KEY,
    eid int PRIMARY KEY,
    status enum ('yes', 'no', 'maybe') NOT NULL
)