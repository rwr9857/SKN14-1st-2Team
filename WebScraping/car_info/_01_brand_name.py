import pickle
import mysql.connector


def create_and_insert_table(unique_brand_names):
    """테이블 생성 및 브랜드 이름 데이터를 삽입하는 함수"""

    # MySQL 데이터베이스 연결
    conn = mysql.connector.connect(
        host="localhost", user="skn14", password="skn14", database="teamdb"
    )
    cursor = conn.cursor()

    # 테이블 생성 (이미 존재하면 무시)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tbl_brand (
            brand_id INT AUTO_INCREMENT PRIMARY KEY,
            brand_name VARCHAR(255) UNIQUE
        )
    """
    )

    # unique_brand_names를 tbl_brand 테이블에 삽입
    for brand_name in unique_brand_names:
        try:
            cursor.execute(
                """
                INSERT INTO tbl_brand (brand_name) VALUES (%s)
            """,
                (brand_name,),
            )
        except mysql.connector.IntegrityError:
            # 이미 존재하는 브랜드 이름은 삽입하지 않음
            pass

    # 변경 사항 저장
    conn.commit()

    # 테이블 전체 조회
    cursor.execute("SELECT * FROM tbl_brand")
    rows = cursor.fetchall()

    # 결과 출력
    print("\n✅ tbl_brand 테이블 전체 조회 결과:")
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


def extract_unique_brand_names(car_info_list):
    """car_info_list에서 고유한 브랜드 이름을 추출하는 함수"""
    return set(car_info.brand for car_info in car_info_list)


def main():
    # car_info_list 불러오기
    car_info_list = load_car_info()

    # car_info_list에서 고유한 브랜드 이름 추출
    unique_brand_names = extract_unique_brand_names(car_info_list)

    # 고유한 브랜드 이름 출력
    print("\n✅ 고유한 브랜드 이름들:")
    print(unique_brand_names)

    # 테이블 생성 및 브랜드 데이터 삽입
    create_and_insert_table(unique_brand_names)


if __name__ == "__main__":
    main()
