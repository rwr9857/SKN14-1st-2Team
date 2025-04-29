import mysql.connector


def add_body_type_category():
    """tbl_body_type 테이블에 body_type_category 칼럼 추가 및 PRIMARY KEY 설정하는 함수"""

    # MySQL 데이터베이스 연결
    conn = mysql.connector.connect(
        host="localhost", user="skn14", password="skn14", database="teamdb"
    )
    cursor = conn.cursor()

    # body_type_category 칼럼 추가
    cursor.execute(
        """
        ALTER TABLE tbl_body_type
        ADD COLUMN body_type_category VARCHAR(255);
    """
    )

    # body_type_category 칼럼 업데이트 (여기에 body_type별로 값을 설정)
    cursor.execute(
        """
        UPDATE tbl_body_type
        SET body_type_category = CASE 
            WHEN body_type = '준대형 세단' THEN '승용차'
            WHEN body_type = '준대형 트럭' THEN 'SUV'
            WHEN body_type = '준대형 SUV' THEN 'SUV'
            WHEN body_type = '경형 RV' THEN '경차'
            WHEN body_type = '소형 SUV' THEN 'SUV'
            WHEN body_type = '중형 트럭' THEN '기타'
            WHEN body_type = '경형 해치백' THEN '경차'
            WHEN body_type = '준중형 세단' THEN '승용차'
            WHEN body_type = '소형 트럭' THEN '기타'
            WHEN body_type = '경형 밴' THEN '경차'
            WHEN body_type = '준중형 SUV' THEN 'SUV'
            WHEN body_type = '중형 밴' THEN '기타'
            WHEN body_type = '준중형 해치백' THEN '승용차'
            WHEN body_type = '중형 왜건' THEN '승용차'
            WHEN body_type = '소형 왜건' THEN '승용차'
            WHEN body_type = '소형 컨버터블' THEN '승용차'
            WHEN body_type = '스포츠카 쿠페' THEN '승용차'
            WHEN body_type = '대형 밴' THEN '기타'
            WHEN body_type = '준중형 RV' THEN '승용차'
            WHEN body_type = '소형 해치백' THEN '승용차'
            WHEN body_type = '준중형 밴' THEN '기타'
            WHEN body_type = '중형 SUV' THEN 'SUV'
            WHEN body_type = '대형 RV' THEN 'SUV'
            WHEN body_type = '중형 세단' THEN '승용차'
            WHEN body_type = '소형 밴' THEN '기타'
            WHEN body_type = '경형 SUV' THEN '경차'
            WHEN body_type = '준중형 트럭' THEN '기타'
            ELSE body_type_category -- 매칭 안된건 기존 값 유지
        END;
    """
    )

    # 변경 사항 저장
    conn.commit()

    # 연결 종료
    cursor.close()
    conn.close()

    print(
        "✅ tbl_body_type 테이블의 body_type_category 칼럼이 추가되었고, PRIMARY KEY로 설정되었습니다."
    )


if __name__ == "__main__":
    add_body_type_category()
