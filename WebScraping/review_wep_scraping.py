from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs

from WebScraping.mysql_connector import db_connection
from DB.dto.car_review_dto import CarReviewDTO
from DB.dto.comment_info_dto import CommentDTO
from DB.dao.car_review_dao import CarReviewDAO
from DB.dao.comment_info_dao import CommentDAO

from datetime import datetime, timedelta
import re


# 설문 조사 사람들 숫자만 가져오기
def get_count_ppl(ppl_unformatted: str) -> int:
    ppl_formatted = "".join(c for c in ppl_unformatted if c.isdigit())
    return int(ppl_formatted)


# 댓글 ~시간전 ~일전 따로 계산하기
def convert_relative_time_to_datetime(relative_time: str) -> str:
    now = datetime.now()  # 현재 시간

    # '일 전', '시간 전', '분 전' 등을 처리하는 정규 표현식
    day_pattern = r"(\d+)일 전"
    hour_pattern = r"(\d+)시간 전"
    minute_pattern = r"(\d+)분 전"

    # '일 전' 처리
    match = re.search(day_pattern, relative_time)
    if match:
        days_ago = int(match.group(1))
        return (now - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")

    # '시간 전' 처리
    match = re.search(hour_pattern, relative_time)
    if match:
        hours_ago = int(match.group(1))
        return (now - timedelta(hours=hours_ago)).strftime("%Y-%m-%d %H:%M:%S")

    # '분 전' 처리
    match = re.search(minute_pattern, relative_time)
    if match:
        minutes_ago = int(match.group(1))
        return (now - timedelta(minutes=minutes_ago)).strftime("%Y-%m-%d %H:%M:%S")

    # 그 외의 경우 (예: '방금')
    return now.strftime("%Y-%m-%d %H:%M:%S")


# 드라이버 실행
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")

# 반드시 Service와 함께 ChromeDriverManager 사용
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 웹페이지 접속
driver.get("https://naver.com")
time.sleep(3)

# URL 수집
url_list = [
    "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=%ED%98%84%EB%8C%80+%EC%BD%94%EB%82%98+%ED%95%98%EC%9D%B4%EB%B8%8C%EB%A6%AC%EB%93%9C+%EC%98%A4%EB%84%88%ED%8F%89%EA%B0%80+&oquery=%ED%91%B8%EC%A1%B0+308+%EC%98%A4%EB%84%88%ED%8F%89%EA%B0%80&tqi=jsG7%2BlqVOsCss77mZshssssstzw-355267&ackey=n7lpg2g6",
]

# 검색어 입력
search_box = driver.find_element(By.ID, "query")
search_box.send_keys("네이버 자동차")
search_box.send_keys(Keys.ENTER)
time.sleep(3)

# 5천만원 이하 필터링
button = driver.find_element(
    By.XPATH,
    '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[1]/div/div/div/ul/li[5]/div/a',
)
button.click()
time.sleep(2)

slider = driver.find_element(
    By.XPATH,
    '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[1]/div/div/div/div/div/div/div[2]/div[1]/div[3]/div/span/span[7]',
)
slider.click()
time.sleep(2)

actions = ActionChains(driver)
for _ in range(2):
    actions.send_keys(Keys.ARROW_LEFT).perform()
time.sleep(2)

apply = driver.find_element(
    By.XPATH,
    '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/a',
)
apply.click()
time.sleep(2)


for i in range(1, 16):
    try:
        # ✅ 컨테이너 안에 info_box만 찾기
        container = driver.find_element(
            By.XPATH,
            '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[3]/div[ ' + str(i) + "]",
        )
        car_list = container.find_elements(By.CSS_SELECTOR, ".info_box")

        for car_tag in car_list:
            link = car_tag.find_element(By.CSS_SELECTOR, "a:first-of-type")
            href = link.get_attribute("href")
            if href:
                url_list.append(href + "%20%EC%98%A4%EB%84%88%ED%8F%89%EA%B0%80")

        next_button = driver.find_element(
            By.XPATH, '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[4]/div/a[2]'
        )
        next_button.click()
        time.sleep(3)

    except Exception as e:
        print(f"오류 발생: {e}")

# 최종 결과 출력
print(f"총 수집된 링크 수: {len(url_list)}개")
print(url_list)

no_review_car_names = []
for url in url_list:
    try:
        driver.get(url)
        time.sleep(3)

        car_review_dao = CarReviewDAO(db_connection)
        try:
            # 차 이름
            car_name = driver.find_element(By.CSS_SELECTOR, ".area_text_title")

            # 평균 점수
            avg_score = driver.find_element(By.CSS_SELECTOR, ".area_star_number._avg")

            # 설문 조사 작성한 사람들 수
            count_ppl = driver.find_element(By.CSS_SELECTOR, ".area_people")

            final_count_ppl = get_count_ppl(count_ppl.text)

            # 그래프 데이터
            graph_info = driver.find_elements(By.CSS_SELECTOR, ".guide._chart_label>li")
            graph_data = []
            for graph in graph_info:
                graph_data.append(graph.text)

            graph_data_text = ",".join(graph_data)

            # DTO 객체 생성
            car_review = CarReviewDTO(
                car_name.text, avg_score.text, final_count_ppl, graph_data_text
            )

            # CarReviewDAO 객체를 사용하여 DB에 저장
            if car_review:
                car_review_id = car_review_dao.insert_car_review(car_review)
                print(f"Inserted car review with ID: {car_review_id}")
            else:
                # 리뷰가 없으면 차 이름을 리스트에 추가
                no_review_car_names.append(car_name.text)

            time.sleep(2)

        except:
            car_review = None

        comment_info_dao = CommentDAO(db_connection)
        try:
            # 댓글 6개
            comment_boxes = driver.find_elements(By.CLASS_NAME, "u_cbox_comment_box")

            for box in comment_boxes[:6]:
                nickname = box.find_element(By.CLASS_NAME, "u_cbox_nick").text
                average_rating = box.find_element(
                    By.CLASS_NAME, "u_cbox_multirating_totalcount_value"
                ).text
                comment_text = box.find_element(By.CLASS_NAME, "u_cbox_contents").text
                date = box.find_element(By.CLASS_NAME, "u_cbox_date").text

                created_at = convert_relative_time_to_datetime(date)

                comment = CommentDTO(
                    car_review_id, nickname, average_rating, comment_text, created_at
                )

                if comment:
                    comment_info_dao.insert_comment(comment)  # 댓글을 DB에 삽입
            time.sleep(2)
        except Exception as e:
            print(f"{url} 에서 오류 발생: {e}")

    except Exception as e:
        print(f"{url} 에서 오류 발생: {e}")

if no_review_car_names:
    print(f"리뷰가 없는 차 이름들: {no_review_car_names}")
