CREATE TABLE IF NOT EXISTS TextLanguages (
    text_id INT,
    language_id INT,
    PRIMARY KEY (text_id, language_id),
    FOREIGN KEY (text_id) REFERENCES Texts(text_id),
    FOREIGN KEY (language_id) REFERENCES Languages(language_id)
);