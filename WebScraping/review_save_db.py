from DB.dto.car_review_dto import CarReviewDTO
from DB.dto.comment_info_dto import CommentDTO
from DB.dao.car_review_dao import CarReviewDAO
from DB.dao.comment_info_dao import CommentDAO
import mysql.connector

# DB 연결
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="teamdb"
)

# CarReviewDTO 객체 생성
car_review = CarReviewDTO(
    "이서님 들어갔어요!!",
    4.5,
    100,
    '주행\n9.8, 가격\n9.4, 거주성\n9.5, 품질\n9.6, 디자인\n9.9, 연비\n9.8'  # 문자열로 넣기
)

# DAO로 car_review 삽입
car_review_dao = CarReviewDAO(db_connection)
car_review_dao.insert_car_review(car_review)  # 이 안에서 review_id 채워야 함!

# car_review.review_id를 써서 댓글 추가
comment = CommentDTO(
    car_review.review_id,
    "이서님 연습중입니다",
    4.0,
    "차가 너무 좋습니다!",
    "2025-04-28 12:00:00"
)
comment_dao = CommentDAO(db_connection)
comment_dao.insert_comment(comment)
