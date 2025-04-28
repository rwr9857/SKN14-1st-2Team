import pickle
import mysql.connector


def add_fuel_type():
    """tbl_fuel_type 테이블에 새로운 행을 추가하는 함수"""

    # MySQL 데이터베이스 연결
    conn = mysql.connector.connect(
        host='localhost',
        user='skn14',
        password='skn14',
        database='teamdb'
    )
    cursor = conn.cursor()

    # INSERT 쿼리 실행
    cursor.execute('''
        INSERT INTO tbl_fuel_type (fuel_type_id, fuel_type)
        VALUES (10, '하이브리드')
    ''')

    # 변경 사항 저장
    conn.commit()

    # 연결 종료
    cursor.close()
    conn.close()

    print("✅ tbl_fuel_type 테이블에 '10'과 '하이브리드'가 성공적으로 추가되었습니다.")


if __name__ == "__main__":
    add_fuel_type()
