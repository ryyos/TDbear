CREATE TABLE IF NOT EXISTS tdbearai (
    id INT NOT NULL,
    user_id INT,
    username VARCHAR(1000),
    bio VARCHAR(1000),
    dates VARCHAR(255),

    question TEXT,
    answer TEXT,
    action VARCHAR(255),
    PRIMARY KEY(id)

)