import pickle
import mysql.connector


def create_tbl_all_data_table():
    """all_data 테이블을 생성하는 함수"""
    conn = mysql.connector.connect(
        host="localhost", user="skn14", password="skn14", database="teamdb"
    )
    cursor = conn.cursor()

    # 테이블 생성 (이미 존재하면 무시)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS all_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            model_name VARCHAR(255),
            body_type VARCHAR(255),
            category_id INT,
            fuel_type_id INT,
            price INT,
            power INT,
            fuel_efficiency FLOAT,
            model_year INT,
            size FLOAT,
            engine_type VARCHAR(255),
            image_link VARCHAR(255),
            brand_id INT
        )
    """
    )

    conn.commit()
    cursor.close()
    conn.close()


def fetch_ids_for_references(body_type, fuel_type, brand_name):
    """brand_name, body_type, fuel_type에 대한 참조 ID 값을 찾아 반환하는 함수"""
    conn = mysql.connector.connect(
        host="localhost", user="skn14", password="skn14", database="teamdb"
    )
    cursor = conn.cursor()

    # brand_id 조회
    cursor.execute(
        "SELECT brand_id FROM tbl_brand WHERE brand_name = %s", (brand_name,)
    )
    brand_id = cursor.fetchone()

    # fuel_type_id 조회 (기본)
    cursor.execute(
        "SELECT fuel_type_id FROM tbl_fuel_type WHERE fuel_type = %s", (fuel_type,)
    )
    fuel_type_id = cursor.fetchone()

    # body_type으로 category_id 조회
    cursor.execute(
        "SELECT category_id FROM tbl_body_type WHERE body_type = %s", (body_type,)
    )
    category_id = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "brand_id": brand_id[0] if brand_id else None,
        "fuel_type_id": fuel_type_id[0] if fuel_type_id else None,
        "category_id": category_id[0] if category_id else None,
    }


def split_fuel_types(fuel_type):
    """연료 타입이 여러 개인 경우 나누는 함수"""
    return [ft.strip() for ft in fuel_type.split(",")]


def save_all_data_to_db(car_info_list):
    """car_info_list의 데이터를 all_data 테이블에 저장하는 함수"""
    conn = mysql.connector.connect(
        host="localhost", user="skn14", password="skn14", database="teamdb"
    )
    cursor = conn.cursor()

    for car_info in car_info_list:
        fuel_types = split_fuel_types(car_info.fuel_type)

        for single_fuel_type in fuel_types:
            ids = fetch_ids_for_references(
                car_info.body_type, single_fuel_type, car_info.brand
            )

            cursor.execute(
                """
                INSERT INTO all_data (
                    model_name, body_type, category_id, fuel_type_id, price, power,
                    fuel_efficiency, model_year, size, engine_type, image_link, brand_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    car_info.model_name,
                    car_info.body_type,
                    ids["category_id"],
                    ids["fuel_type_id"],
                    car_info.price,
                    car_info.power,
                    car_info.fuel_efficiency,
                    car_info.model_year,
                    car_info.size,
                    car_info.engine_type,
                    car_info.image_link,
                    ids["brand_id"],
                ),
            )

    conn.commit()
    cursor.close()
    conn.close()


def load_car_info():
    """car_info_list.pkl 파일에서 데이터를 불러오는 함수"""
    with open("car_info_list.pkl", "rb") as f:
        car_info_list = pickle.load(f)
    return car_info_list


def main():
    car_info_list = load_car_info()
    create_tbl_all_data_table()
    save_all_data_to_db(car_info_list)
    print("✅ all_data 테이블에 데이터 삽입이 완료되었습니다.")


if __name__ == "__main__":
    main()
