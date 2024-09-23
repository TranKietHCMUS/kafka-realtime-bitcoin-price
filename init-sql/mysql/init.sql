ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1511'; 

USE bitcoin;

CREATE TABLE binance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,
    crawl_at DATETIME NOT NULL
);