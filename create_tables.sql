CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    notification_preference BOOLEAN DEFAULT 0
);

CREATE TABLE favorite_artists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    artist_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE concerts (
    concert_id INT AUTO_INCREMENT PRIMARY KEY,
    concert_name VARCHAR(200) NOT NULL,
    event_date DATE NOT NULL,
    location VARCHAR(100) NOT NULL
);

CREATE TABLE user_concerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    concert_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (concert_id) REFERENCES concerts(concert_id)
);



