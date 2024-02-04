CREATE TABLE IF NOT EXISTS tdbear (
    id INT NOT NULL,
    user_id INT,
    username VARCHAR(1000),
    bio VARCHAR(1000),
    dates VARCHAR(255),

    action VARCHAR(255),
    key_search VARCHAR(1000),
    format VARCHAR(50),
    amount INT,
    PRIMARY KEY(id)
);