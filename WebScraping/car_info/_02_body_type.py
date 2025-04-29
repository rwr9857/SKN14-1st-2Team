import pickle
import mysql.connector


def create_and_insert_table(unique_body_types):
    """tbl_body_type 테이블을 생성하고, 고유한 body_type 데이터를 삽입하는 함수"""

    # MySQL 데이터베이스 연결
    conn = mysql.connector.connect(
        host="localhost", user="skn14", password="skn14", database="teamdb"
    )
    cursor = conn.cursor()

    # 테이블 생성 (이미 존재하면 무시)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tbl_body_type (
            body_type_id INT AUTO_INCREMENT PRIMARY KEY,  # 고유 ID
            body_type VARCHAR(255) UNIQUE                 # 고유한 body_type
        )
    """
    )

    # 테이블에 고유한 body_type 삽입
    for body_type in unique_body_types:
        try:
            cursor.execute(
                """
                INSERT INTO tbl_body_type (body_type) VALUES (%s)
            """,
                (body_type,),
            )
        except mysql.connector.IntegrityError:
            # 이미 존재하는 body_type은 삽입하지 않음
            pass

    # 변경 사항 저장
    conn.commit()

    # 테이블 전체 조회
    cursor.execute("SELECT * FROM tbl_body_type")
    rows = cursor.fetchall()

    # 결과 출력
    print("\n✅ tbl_body_type 테이블 전체 조회 결과:")
    for row in rows:
        print(row)

    # 연결 종료
    cursor.close()
    conn.close()


def load_car_info():
    """car_info_list.pkl 파일에서 데이터를 불러오는 함수"""
    with open("car_info_list.pkl", "rb") as f:
        car_info_list = pickle.load(f)

    return car_info_list


def extract_unique_body_types(car_info_list):
    """car_info_list에서 고유한 body_type 값을 추출하는 함수"""
    return set(car_info.body_type for car_info in car_info_list)


def main():
    """전체 흐름을 실행하는 main 함수"""
    # car_info_list 불러오기
    car_info_list = load_car_info()

    # 고유한 body_type 추출
    unique_body_types = extract_unique_body_types(car_info_list)

    # 고유한 body_type 출력
    print("\n✅ 고유한 body_type들:")
    print(unique_body_types)

    # tbl_body_type 테이블 생성 및 데이터 삽입
    create_and_insert_table(unique_body_types)


if __name__ == "__main__":
    main()
