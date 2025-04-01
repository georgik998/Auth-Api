CREATE TYPE sextape AS ENUM ('m', 'f');  -- on of favorite track btw

CREATE TABLE IF NOT EXISTS users(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    phone_number VARCHAR(21) UNIQUE NOT NULL ,
    email VARCHAR(64) UNIQUE NOT NULL,
    password TEXT NOT NULL,

    sex sextape NOT NULL,
    full_name VARCHAR(64),
    is_ban BOOLEAN  NOT NULL DEFAULT FALSE,
    registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);