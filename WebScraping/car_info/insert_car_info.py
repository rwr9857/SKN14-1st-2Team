import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306, # 기본포트 3306인 경우 생략 가능
    user='skn14',
    password='skn14',
    database='teamdb'
)

cursor = conn.cursor()

# 커서를 통한 쿼리 수행
cursor.execute('select * from car_info')
rows = cursor.fetchall() # 결과집합 반환
for row in rows:
    print(row)

cursor.close()
conn.close()
