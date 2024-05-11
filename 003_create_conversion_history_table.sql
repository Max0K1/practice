CREATE TABLE IF NOT EXISTS ConversionHistory (
    conversion_id INT PRIMARY KEY AUTO_INCREMENT,
    text_id INT,
    user_id INT,
    conversion_date DATE,
    input_text TEXT,
    output_audio_path VARCHAR(255),
    FOREIGN KEY (text_id) REFERENCES Texts(text_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);