--
-- File generated with SQLiteStudio v3.4.4 on Tue Aug 22 20:22:46 2023
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: rooms
CREATE TABLE IF NOT EXISTS rooms (
    id          INTEGER,
    name        TEXT,
    ip          TEXT    UNIQUE,
    description TEXT,
    PRIMARY KEY (
        id AUTOINCREMENT
    )
);

INSERT INTO rooms (
                      id,
                      name,
                      ip,
                      description
                  )
                  VALUES (
                      445,
                      'room0',
                      '192.168.31.1',
                      NULL
                  );

INSERT INTO rooms (
                      id,
                      name,
                      ip,
                      description
                  )
                  VALUES (
                      446,
                      'room1',
                      '192.168.31.11',
                      NULL
                  );

INSERT INTO rooms (
                      id,
                      name,
                      ip,
                      description
                  )
                  VALUES (
                      447,
                      'room2',
                      '192.168.31.125',
                      NULL
                  );

INSERT INTO rooms (
                      id,
                      name,
                      ip,
                      description
                  )
                  VALUES (
                      448,
                      'room3',
                      '192.168.31.127',
                      NULL
                  );


-- Table: users
CREATE TABLE IF NOT EXISTS users (
    username TEXT    NOT NULL
                     UNIQUE,
    password TEXT,
    id       INTEGER UNIQUE,
    role     INTEGER,
    PRIMARY KEY (
        id AUTOINCREMENT
    )
);

INSERT INTO users (
                      username,
                      password,
                      id,
                      role
                  )
                  VALUES (
                      'admin',
                      'admin',
                      1,
                      1
                  );

INSERT INTO users (
                      username,
                      password,
                      id,
                      role
                  )
                  VALUES (
                      'user',
                      'user',
                      3,
                      0
                  );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
