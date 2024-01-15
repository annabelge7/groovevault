CREATE DATABASE IF NOT EXISTS groovevault;

USE groovevault;

DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS playlists;
DROP TABLE IF EXISTS playlistsongs;

CREATE TABLE users
(
    userid       int not null AUTO_INCREMENT,
    username     varchar(64) not null,
    PRIMARY KEY  (userid),
    UNIQUE       (username)
);

ALTER TABLE users AUTO_INCREMENT = 1;  -- starting value

CREATE TABLE songs
(
    songid       int not null AUTO_INCREMENT,
    songname     varchar(64) not null,
    artist       varchar(64) not null,
    album        varchar(64) not null,
    originalsongfile    varchar(256) not null,  -- original name from user
    songfilekey         varchar(256) not null,  -- filename in the bucket
    PRIMARY KEY  (songid),
    UNIQUE       (songfilekey)
);

ALTER TABLE songs AUTO_INCREMENT = 1;  -- starting value

CREATE TABLE playlists
(
    playlistid        int not null AUTO_INCREMENT,
    playlistname      varchar(256) not null,
    userid            int not null,
    PRIMARY KEY (playlistid),
    FOREIGN KEY (userid) REFERENCES users(userid)
);

ALTER TABLE playlists AUTO_INCREMENT = 1;  -- starting value

CREATE TABLE playlistsongs
(
  playlistid          int not null,
  songid              int not null,
  FOREIGN KEY (playlistid) REFERENCES playlists(playlistid),
  FOREIGN KEY (songid) REFERENCES songs(songid)
)

--
-- Insert some users to start with:
-- 
-- PWD hashing: https://phppasswordhash.com/
--

  
INSERT INTO users(username)  -- pwd = abc123!!
            values('jenna');

INSERT INTO users(username)  -- pwd = abc456!!
            values('annabel');

INSERT INTO users(username)  -- pwd = abc789!!
            values('varoon');

INSERT INTO users(username)  -- pwd = abc789!!
            values('gillian');


--
-- adds two users to the database, one for read-only access and
-- another for read-write access:
--
-- NOTE: do NOT change the user names, and do NOT change the pwds.
-- These need to remain as is for grading purposes.
--
-- ref: https://dev.mysql.com/doc/refman/8.0/en/create-user.html
--

-- USE photoapp;

-- DROP USER IF EXISTS 'photoapp-read-only';
-- DROP USER IF EXISTS 'photoapp-read-write';

-- CREATE USER 'photoapp-read-only' IDENTIFIED BY 'abc123!!';
-- CREATE USER 'photoapp-read-write' IDENTIFIED BY 'def456!!';

-- GRANT SELECT, SHOW VIEW ON photoapp.* 
--       TO 'photoapp-read-only';
-- GRANT SELECT, SHOW VIEW, INSERT, UPDATE, DELETE ON photoapp.* 
--       TO 'photoapp-read-write';

-- FLUSH PRIVILEGES;

--
-- creating user accounts for database access:
--
-- ref: https://dev.mysql.com/doc/refman/8.0/en/create-user.html
--

DROP USER IF EXISTS 'groovevault-read-only';
DROP USER IF EXISTS 'groovevault-read-write';

CREATE USER 'groovevault-read-only' IDENTIFIED BY 'abc123!!';
CREATE USER 'groovevault-read-write' IDENTIFIED BY 'def456!!';

GRANT SELECT, SHOW VIEW ON groovevault.* 
      TO 'groovevault-read-only';
GRANT SELECT, SHOW VIEW, INSERT, UPDATE, DELETE, DROP, CREATE, ALTER ON groovevault.* 
      TO 'groovevault-read-write';

FLUSH PRIVILEGES;

--
-- done
--


SHOW TABLES;
