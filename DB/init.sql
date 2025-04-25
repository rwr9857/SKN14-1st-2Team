CREATE DATABASE teamdb;


CREATE TABLE car_info (
    car_id INT NOT NULL AUTO_INCREMENT,
    car_model VARCHAR(100),
    car_body_type VARCHAR(100),
    car_fuel_type VARCHAR(100),
    car_price INT,
    car_horsepower INT,
    car_engine_type VARCHAR(20),
    car_fuel_efficiency VARCHAR(100),
    car_size VARCHAR(50),
    car_img_url VARCHAR(100),
    car_brand VARCHAR(50),
    PRIMARY KEY (car_id)
);


CREATE TABLE user_info (
    user_id INT NOT NULL AUTO_INCREMENT,
    user_age INT,
    user_gender VARCHAR(10),
    car_id INT,
    PRIMARY KEY (user_id),
    FOREIGN KEY (car_id) REFERENCES car_info(car_id)
);




