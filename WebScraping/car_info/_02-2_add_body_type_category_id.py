import mysql.connector

def add_category_id():
    """tbl_body_type 테이블에 category_id 칼럼 추가 및 PRIMARY KEY 설정하는 함수"""

    # MySQL 데이터베이스 연결
    conn = mysql.connector.connect(
        host='localhost',
        user='skn14',
        password='skn14',
        database='teamdb'
    )
    cursor = conn.cursor()

    # category_id 칼럼 추가
    cursor.execute('''
        ALTER TABLE tbl_body_type
        ADD COLUMN category_id INT;
    ''')

    # category_id 칼럼에 데이터 업데이트
    cursor.execute('''
        UPDATE tbl_body_type
        SET category_id = CASE 
            WHEN body_type_category = '경차' THEN 1 
            WHEN body_type_category = '승용차' THEN 2  
            WHEN body_type_category = 'SUV' THEN 3  
            WHEN body_type_category = '기타' THEN 4  
            ELSE Null
        END;
    ''')

    # 변경 사항 저장
    conn.commit()

    # 연결 종료
    cursor.close()
    conn.close()

    print("✅ tbl_body_type 테이블에 category_id 칼럼이 추가되었고, category_id가 PRIMARY KEY로 설정되었습니다.")

if __name__ == "__main__":
    add_category_id()
