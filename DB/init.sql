DROP TABLE IF EXISTS USER_INFO;
DROP TABLE IF EXISTS CAR_INFO;
DROP TABLE IF EXISTS FUEL_TYPE_INFO;
DROP TABLE IF EXISTS MODEL_TYPE_INFO;
DROP TABLE IF EXISTS BODY_TYPE_INFO;
DROP TABLE IF EXISTS ENGINE_INFO;
DROP TABLE IF EXISTS BRAND_INFO;

use teamdb;
# grant all privileges on teamdb.* to 'ryuuung'@'%';

-- 브랜드 정보
CREATE TABLE BRAND_INFO (
    BRAND_ID INT AUTO_INCREMENT PRIMARY KEY ,
    BRAND_NAME VARCHAR(30) NOT NULL
);

# -- 엔진 정보 # 엔진정보 ex) l4 자연흡기 이런거 뺌 car_info 에 넣을 예정
# CREATE TABLE ENGINE_INFO (
#     ENGINE_ID INT AUTO_INCREMENT PRIMARY KEY ,
#     ENGINE_NAME VARCHAR(30) NOT NULL
# );

-- 바디 타입 정보
CREATE TABLE BODY_TYPE_INFO (
    BODY_TYPE_ID INT AUTO_INCREMENT PRIMARY KEY ,
    BODY_TYPE_NAME VARCHAR(30)
);

-- 모델명 정보
CREATE TABLE MODEL_TYPE_INFO (
    MODEL_TYPE_ID INT AUTO_INCREMENT PRIMARY KEY ,
    MODEL_TYPE_NAME VARCHAR(30)
);

-- 연료 정보
CREATE TABLE FUEL_TYPE_INFO (
    FUEL_TYPE_ID INT AUTO_INCREMENT PRIMARY KEY ,
    FUEL_TYPE_NAME VARCHAR(30)
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
    CAR_HORSEPOWER INT,
    CAR_FUEL_EFFICIENCY INT,
    CAR_MODEL_YEAR INT,
    CAR_SIZE INT,
    CAR_ENGINE_TYPE varchar(40),
    CAR_IMG_URL VARCHAR(100),
    FOREIGN KEY (CAR_MODEL) REFERENCES MODEL_TYPE_INFO(MODEL_TYPE_ID),
    FOREIGN KEY (CAR_BRAND) REFERENCES  BRAND_INFO(BRAND_ID),
    FOREIGN KEY (CAR_BODY_TYPE) REFERENCES BODY_TYPE_INFO(BODY_TYPE_ID),
#     FOREIGN KEY (CAR_ENGINE_TYPE) REFERENCES ENGINE_INFO(ENGINE_ID),
    FOREIGN KEY (CAR_FUEL_TYPE) REFERENCES FUEL_TYPE_INFO(FUEL_TYPE_ID)
);

-- 유저 정보
CREATE TABLE USER_INFO (
    USER_ID INT AUTO_INCREMENT PRIMARY KEY ,
    USER_AGE INT NOT NULL ,
    USER_GENDER VARCHAR(10) NOT NULL CHECK (USER_GENDER IN ('남', '여')),
    CAR_ID INT NOT NULL,
    FOREIGN KEY (CAR_ID) REFERENCES CAR_INFO(CAR_ID)
);

insert into BRAND_INFO (BRAND_NAME)
values
    ('현대'),
    ('기아'),
    ('제네시스'),
    ('르노코리아'),
    ('KGM'),
    ('폭스바겐'),
    ('메르세데스 벤츠'),
    ('BMW'),
    ('아우디'),
    ('토요타'),
    ('혼다'),
    ('볼보'),
    ('미니'),
    ('쉐보레'),
    ('지프'),
    ('르노'), # 뭐가 다른지 모르겠음
    ('푸조');

insert into body_type_info (BODY_TYPE_NAME)
values ('경차'),
       ('승용차'),
       ('SUV'),
       ('기타');

insert into model_type_info (MODEL_TYPE_NAME)
values ('모닝'),
       ('레이'),
       ('스파크'),
       ('아반떼'),
       ('K3'),
       ('K5'),
       ('K8'),
       ('쏘나타'),
       ('그랜저'),
       ('아이오닉'),
       ('제네시스');

insert into fuel_type_info(FUEL_TYPE_NAME)
values ('디젤'),
       ('가솔린'),
       ('하이브리드'),
       ('전기차');