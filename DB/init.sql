# DROP TABLE IF EXISTS USER_INFO;
# DROP TABLE IF EXISTS CAR_INFO;
# DROP TABLE IF EXISTS FUEL_TYPE_INFO;
# DROP TABLE IF EXISTS MODEL_TYPE_INFO;
# DROP TABLE IF EXISTS BODY_TYPE_INFO;
# DROP TABLE IF EXISTS ENGINE_INFO;
# DROP TABLE IF EXISTS BRAND_INFO;
# drop table if exists car_review_info;
# drop table if exists comment_info;
# drop table if exists job_type_info;

-- 브랜드 정보
CREATE TABLE BRAND_INFO (
    BRAND_ID INT AUTO_INCREMENT PRIMARY KEY ,
    BRAND_NAME VARCHAR(30) NOT NULL
);

-- 바디 타입 정보
CREATE TABLE BODY_TYPE_INFO (
    BODY_TYPE_ID INT AUTO_INCREMENT PRIMARY KEY ,
    BODY_TYPE_NAME VARCHAR(30) NOT NULL
);

-- 모델명 정보
CREATE TABLE MODEL_TYPE_INFO (
    MODEL_TYPE_ID INT AUTO_INCREMENT PRIMARY KEY ,
    MODEL_TYPE_NAME VARCHAR(30) NOT NULL
);

-- 연료 정보
CREATE TABLE FUEL_TYPE_INFO (
    FUEL_TYPE_ID INT AUTO_INCREMENT PRIMARY KEY ,
    FUEL_TYPE_NAME VARCHAR(30) NOT NULL
);

-- 직업정보
create table JOB_TYPE_INFO (
    job_id int auto_increment primary key ,
    job_name varchar(20)
);

-- 자동차 정보
CREATE TABLE CAR_INFO (
    CAR_ID INT AUTO_INCREMENT PRIMARY KEY ,
    CAR_FULL_NAME VARCHAR(100) ,
    CAR_MODEL INT,
    CAR_BRAND INT,
    CAR_BODY_TYPE INT,
    CAR_FUEL_TYPE INT,
    CAR_PRICE INT,
    CAR_HORSEPOWER FLOAT,
    CAR_FUEL_EFFICIENCY FLOAT,
    CAR_MODEL_YEAR INT,
    CAR_SIZE FLOAT,
    CAR_ENGINE_TYPE varchar(40),
    CAR_IMG_URL VARCHAR(100),
    FOREIGN KEY (CAR_MODEL) REFERENCES MODEL_TYPE_INFO(MODEL_TYPE_ID),
    FOREIGN KEY (CAR_BRAND) REFERENCES  BRAND_INFO(BRAND_ID),
    FOREIGN KEY (CAR_BODY_TYPE) REFERENCES BODY_TYPE_INFO(BODY_TYPE_ID),
    FOREIGN KEY (CAR_FUEL_TYPE) REFERENCES FUEL_TYPE_INFO(FUEL_TYPE_ID)
);

-- 유저 정보
CREATE TABLE USER_INFO (
    USER_ID INT AUTO_INCREMENT PRIMARY KEY ,
    USER_AGE INT NOT NULL ,
    USER_GENDER VARCHAR(10) NOT NULL CHECK (USER_GENDER IN ('남', '여')),
    user_job int NOT NULL ,
    user_purpose VARCHAR(20) NOT NULL ,
    foreign key (user_job) references JOB_TYPE_INFO(job_id)
);

-- 유저가 받은 추천차
CREATE TABLE car_recommendation_info (
    reco_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    car_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user_info(user_id),
    FOREIGN KEY (car_id) REFERENCES car_info(car_id)
);

-- 차의 리뷰
create table car_review_info (
    review_id int auto_increment primary key ,
    car_id int,
    car_name varchar(100) not null,
    avg_score float not null,
    survey_people_count int,
    graph_info varchar(100),
    foreign key (car_id) references car_info(car_id)
);

-- 리뷰의 댓글
create table comment_info (
    comment_id int auto_increment primary key ,
    review_id int not null,
    nickname varchar(20) not null,
    comment_avg_score float,
    comment_text varchar(300),
    created_at varchar(20)
);

INSERT INTO JOB_TYPE_INFO (job_name) VALUES
('대학생'),
('사무직'),
('IT/개발'),
('서비스직'),
('생산직'),
('기타');

