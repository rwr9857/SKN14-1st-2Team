# 모든 정보 조회
select *
from teamdb.car_info;

# 세번째 페이지 정보 조회
SELECT c.CAR_FULL_NAME       '자동차명',
       c.CAR_PRICE           '가격',
       f.FUEL_TYPE_NAME      '연료타입',
       c.CAR_FUEL_EFFICIENCY '연비',
       c.CAR_HORSEPOWER      '출력',
       c.CAR_ENGINE_TYPE     '엔진'
FROM teamdb.car_info c
         LEFT JOIN teamdb.fuel_type_info f ON c.CAR_FUEL_TYPE = f.FUEL_TYPE_ID
WHERE c.CAR_PRICE BETWEEN 2000 AND 4000
  AND c.CAR_FUEL_TYPE = 2
  AND c.CAR_BODY_TYPE = 3
ORDER BY c.CAR_FUEL_EFFICIENCY
LIMIT 3;






# 네번째 페이지 정보 조회
SELECT
    c.CAR_ID,
    c.CAR_FULL_NAME,
    b.BRAND_NAME,
    m.MODEL_TYPE_NAME,
    bt.BODY_TYPE_NAME,
    f.FUEL_TYPE_NAME,
    c.CAR_PRICE,
    c.CAR_FUEL_EFFICIENCY
FROM CAR_INFO c
JOIN BRAND_INFO b ON c.CAR_BRAND = b.BRAND_ID
JOIN MODEL_TYPE_INFO m ON c.CAR_MODEL = m.MODEL_TYPE_ID
JOIN BODY_TYPE_INFO bt ON c.CAR_BODY_TYPE = bt.BODY_TYPE_ID
JOIN FUEL_TYPE_INFO f ON c.CAR_FUEL_TYPE = f.FUEL_TYPE_ID
WHERE 1=1
# 이렇게 1=1 이라고만 하고 이 밑에는 사용자에 따라서 선택하면 정보를 볼수있게
  AND bt.BODY_TYPE_NAME = 'SUV'
  AND c.CAR_PRICE BETWEEN 2000 AND 5000
  AND c.CAR_FUEL_EFFICIENCY >= 12
  AND c.CAR_FUEL_EFFICIENCY >= 14
  AND f.FUEL_TYPE_NAME IN ('가솔린', '하이브리드')
ORDER BY c.CAR_PRICE;


/*
파이썬 이런식!
L = m.MODEL_TYPE_ID
JOIN BODY_TYPE_INFO bt ON c.CAR_BODY_TYPE = bt.BODY_TYPE_ID
JOIN FUEL_TYPE_INFO f ON c.CAR_FUEL_TYPE = f.FUEL_TYPE_ID
WHERE 1=1
"""

# 사용자가 선택한 옵션
body_type = "SUV"             # or None
min_price = 2000              # or None
max_price = 5000              # or None
min_efficiency = 14           # or None
fuel_types = ["가솔린", "하이브리드"]  # or None

# 조건 추가
if body_type:
    query += f" AND bt.BODY_TYPE_NAME = '{body_type}'"
if min_price and max_price:
    query += f" AND c.CAR_PRICE BETWEEN {min_price} AND {max_price}"
if min_efficiency:
    query += f" AND c.CAR_FUEL_EFFICIENCY >= {min_efficiency}"
if fuel_types:
    fuel_list = "', '".join(fuel_types)
    query += f" AND f.FUEL_TYPE_NAME IN ('{fuel_list}')"

query += " ORDER BY c.CAR_PRICE"
*/




