CREATE TABLE users 
(
    id SERIAL PRIMARY KEY, 
    username VARCHAR(10) UNIQUE NOT NULL, 
    hashed_password VARCHAR(255) NOT NULL,
    kdnumber INT NOT NULL,
    permission BOOLEAN DEFAULT false, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE kingdoms
(
    kdnumber INT PRIMARY KEY,
    hashed_password VARCHAR(255) NOT NULL,
    permission BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
