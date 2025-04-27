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


if __name__ == "__main__":

    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql",
        database="teamdb"
    )

    # CarReviewDAO 객체 생성
    dao = CarReviewDAO(db_connection)

    # get_car_reviews 호출하여 데이터 조회
    reviews = dao.get_car_reviews()

    print(len(reviews))

    # 반환된 데이터 출력
    for review in reviews:
        print(review)

    # 연결 종료
    db_connection.close()

