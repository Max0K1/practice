CREATE TABLE IF NOT EXISTS Texts (
    text_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    text_content TEXT,
    creation_date DATE,
    modification_date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);