import mysql.connector
from DB.dto.car_review_dto import CarReviewDTO


class CarReviewDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_car_reviews(self):
        query = "SELECT car_name, avg_score, survey_people_count, graph_info FROM car_review_info"
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return [CarReviewDTO(*row) for row in result]

    def insert_car_review(self, car_review):
        try:
            cursor = self.db_connection.cursor()
            query = """INSERT INTO car_review_info (car_name, avg_score, survey_people_count, graph_info)
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(
                query,
                (
                    car_review.car_name,
                    car_review.avg_score,
                    car_review.survey_people_count,
                    car_review.graph_info,
                ),
            )
            self.db_connection.commit()
            car_review.review_id = cursor.lastrowid  # 마지막 id 찾기
            return car_review.review_id
        except Exception as e:
            print(f"Error while inserting car review: {e}")
        finally:
            cursor.close()


# 출력 확인 완료
# if __name__ == "__main__":
#
#     db_connection = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="mysql",
#         database="teamdb"
#     )
#
#     # CarReviewDAO 객체 생성
#     dao = CarReviewDAO(db_connection)
#
#     # get_car_reviews 호출하여 데이터 조회
#     reviews = dao.get_car_reviews()
#
#     print(len(reviews))
#
#     # 반환된 데이터 출력
#     for review in reviews:
#         print(review)
#
#     # 연결 종료
#     db_connection.close()
