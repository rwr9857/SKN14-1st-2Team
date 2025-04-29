from DTO.car_review_dto import CarReviewDTO


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
            query = """
                INSERT INTO car_review_info (car_name, avg_score, survey_people_count, graph_info)
                       VALUES (%s, %s, %s, %s)
                """
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