USE teamdb;
# DROP TABLE IF EXISTS all_data;

# #desc tbl_all_data;
#
# # USE teamdb;
# # ALTER TABLE tbl_body_type
# # #DROP COLUMN body_type_category,
# # DROP COLUMN category_id;
#
# # DROP TABLE IF EXISTS user_info;
# # DROP TABLE IF EXISTS car_info;
#
# RENAME TABLE
#     all_data TO car_info,
#     tbl_brand TO brand_info,
#     tbl_body_type TO body_type_info,
#     tbl_fuel_type TO fuel_type_info;
#
# ALTER TABLE body_type_info
# CHANGE COLUMN body_type_id body_id INT NOT NULL,
# CHANGE COLUMN body_type body_name VARCHAR(255) NOT NULL;
#
#
# ALTER TABLE fuel_type_info
# CHANGE COLUMN fuel_type fuel_type_name VARCHAR(255) NOT NULL;
#
#
# ALTER TABLE car_info
# CHANGE COLUMN id car_id INT NOT NULL AUTO_INCREMENT,
# CHANGE COLUMN model_name car_full_name VARCHAR(255),
# CHANGE COLUMN body_type car_body_type VARCHAR(255),
# CHANGE COLUMN fuel_type_id car_fuel_type INT,
# CHANGE COLUMN price car_price VARCHAR(255),
# CHANGE COLUMN power car_horsepower VARCHAR(255),
# CHANGE COLUMN fuel_efficiency car_fuel_efficiency VARCHAR(255),
# CHANGE COLUMN model_year car_model_year VARCHAR(255),
# CHANGE COLUMN size car_size VARCHAR(255),
# CHANGE COLUMN engine_type car_engine_type VARCHAR(255),
# CHANGE COLUMN image_link car_img_url VARCHAR(255);


# alter table car_info
# change column brand_id car_brand INT;
#
# ALTER TABLE brand_info
# MODIFY COLUMN brand_name VARCHAR(255) NOT NULL,
# MODIFY COLUMN brand_id INT NOT NULL;
#
# ALTER TABLE car_info
# MODIFY COLUMN car_id INT NOT NULL;
#
# ALTER TABLE body_type_info
# MODIFY COLUMN body_name VARCHAR(255) NOT NULL,
# MODIFY COLUMN body_id INT NOT NULL;
#
# ALTER TABLE fuel_type_info
# MODIFY COLUMN fuel_type_name VARCHAR(255) NOT NULL,
# MODIFY COLUMN fuel_type_id INT NOT NULL;
#
# -- car_brand를 brand_info 테이블의 brand_id와 연결
# ALTER TABLE car_info
# ADD CONSTRAINT fk_car_brand
# FOREIGN KEY (car_brand) REFERENCES brand_info(brand_id);
#
# -- car_fuel_type을 fuel_type_info 테이블의 fuel_id와 연결
# ALTER TABLE car_info
# ADD CONSTRAINT fk_car_fuel_type
# FOREIGN KEY (car_fuel_type) REFERENCES fuel_type_info(fuel_type_id);
#
#
#
# ALTER TABLE car_recommendation_info
# DROP FOREIGN KEY car_recommendation_info_ibfk_2;
#
# ALTER TABLE car_review_info
# DROP FOREIGN KEY car_review_info_ibfk_1;
#
# ALTER TABLE car_info
# MODIFY COLUMN car_id INT NOT NULL;
#
# ALTER TABLE car_review_info
# ADD CONSTRAINT fk_car_review_info_car_id
# FOREIGN KEY (car_id) REFERENCES car_info(car_id);
#
# ALTER TABLE car_recommendation_info
# ADD CONSTRAINT car_recommendation_info_ibfk_2
# FOREIGN KEY (car_id) REFERENCES car_info(car_id);


# alter table comment_info add constraint fk_comment_info foreign key (review_id) references car_review_info(review_id);
#
# # 리뷰 자동차 이름을 통해 ID 찾아 연결하기
# update car_review_info cri
# join car_info ci on cri.car_name = ci.CAR_FULL_NAME
# set cri.car_id = ci.CAR_ID
# where cri.car_id is null;
