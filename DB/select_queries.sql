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
def make_query(price_range=None, min_efficiency=None, body_type=None, fuel_types=None):
    query = """
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
    """

    if price_range:
        query += f" AND c.CAR_PRICE BETWEEN {price_range[0]} AND {price_range[1]}"
    if min_efficiency:
        query += f" AND c.CAR_FUEL_EFFICIENCY >= {min_efficiency}"
    if body_type:
        query += f" AND bt.BODY_TYPE_NAME = '{body_type}'"
    if fuel_types:
        fuels = "', '".join(fuel_types)
        query += f" AND f.FUEL_TYPE_NAME IN ('{fuels}')"

    query += " ORDER BY c.CAR_PRICE"
    return query
*/

# 리뷰 자동차 이름을 통해 ID 찾아 연결하기
update car_review_info cri
join car_info ci on cri.car_name = ci.CAR_FULL_NAME
set cri.car_id = ci.CAR_ID
where cri.car_id is null;

# 자동차 id를 통해 리뷰 정보

select
    car_name '자동차 이름',
    avg_score '평점',
    survey_people_count '설문 인원수',
    graph_info '그래프 정보'
from car_review_info cri join car_info ci on cri.car_name = ci.CAR_FULL_NAME;


# 리뷰 댓글 정보

select
    nickname '닉네임',
    comment_avg_score '평점',
    comment_text '댓글',
    created_at '작성시간'
from car_review_info cri join comment_info ci on cri.review_id = ci.review_id
