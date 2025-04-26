from DB.db_conn import Database
from DTO.car_info_dto import CarInfoDTO


class CarInfoDAO:
    def __init__(self):
        self.conn = Database().get_connection()

    def get_all_cars(self) -> list[CarInfoDTO]:
        query = """
            SELECT * FROM car_info
        """

        cars = []
        cursor = self.conn.cursor()

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                if len(row) < 10:
                    row = row + ("",) * (10 - len(row))  # 필드 수 부족 시 채우기
                cars.append(CarInfoDTO(*row))  # DTO 객체로 변환
        finally:
            cursor.close()

        return cars
