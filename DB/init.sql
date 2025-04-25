
CREATE DATABASE teamdb;

<<<<<<< HEAD
show databases;

show schemas;

select user, host from user;

create user 'ryunnng'@'%' identified  by 'df1462';
grant all privileges on teamdb.* to 'ryunnng'@'%';
FLUSH PRIVILEGES;

# drop table if exists user_info;
# drop table if exists car_info;

# 브랜드 정보
create table brand_info (
    brand_id int auto_increment primary key ,
    brand_name varchar(30) not null
);

# 엔진 정보
create table engine_info (
    engine_id int auto_increment primary key ,
    engine_name varchar(30) not null
);

# 바디 타입 정보
create table body_type_info (
    body_type_id int auto_increment primary key ,
    body_type_name varchar(30)
);

# 모델명 정보
create table model_type_info (
    model_type_id int auto_increment primary key ,
    model_type_name varchar(30)
);

# 연료 정보
create table fuel_type_info (
    fuel_type_id int auto_increment primary key ,
    fuel_type_name varchar(30)
);

# 자동차 정보
create table car_info (
    car_id int auto_increment primary key ,
    car_full_name varchar(100) ,
    car_model int,
    car_brand int,
    car_body_type int,
    car_engine_type int,
    car_fuel_type int,
    car_price int,
    car_horsepower int,
    car_fuel_efficiency int,
    car_size int,
    car_img_url varchar(100),
    foreign key (car_model) references model_type_info(model_type_id),
    foreign key (car_brand) references  brand_info(brand_id),
    foreign key (car_body_type) references body_type_info(body_type_id),
    foreign key (car_engine_type) references engine_info(engine_id),
    foreign key (car_fuel_type) references fuel_type_info(fuel_type_id)
);

# 유저 정보
create table user_info (
    user_id int auto_increment primary key ,
    user_age int not null ,
    user_gender varchar(10) not null check (user_gender in ('남', '여')),
    car_id int not null,
    foreign key (car_id) references car_info(car_id)
=======
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
>>>>>>> 52209cb24a6067dc493b4eef3e2e71e65578ed15
);






