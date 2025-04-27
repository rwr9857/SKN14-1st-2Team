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

from WebScraping.review_save_db import db_connection # ??

# 드라이버 실행
options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')

# 반드시 Service와 함께 ChromeDriverManager 사용
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 웹페이지 접속
driver.get("https://naver.com")
time.sleep(3)


# # 검색어 입력
# search_box = driver.find_element(By.ID, "query")
# search_box.send_keys("네이버 자동차")
# search_box.send_keys(Keys.ENTER)
# time.sleep(3)
#
# # 5천만원 이하 필터링
# button = driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[1]/div/div/div/ul/li[5]/div/a')
# button.click()
# time.sleep(2)
#
# slider = driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[1]/div/div/div/div/div/div/div[2]/div[1]/div[3]/div/span/span[7]')
# slider.click()
# time.sleep(2)
#
# actions = ActionChains(driver)
# for _ in range(2):
#     actions.send_keys(Keys.ARROW_LEFT).perform()
# time.sleep(2)
#
# apply = driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/a')
# apply.click()
# time.sleep(2)
#
# # URL 수집
# url_list = []
#
# for i in range(1, 16):
#     try:
#         # ✅ 컨테이너 안에 info_box만 찾기
#         container = driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[3]/div[ '+ str(i) + ']')
#         car_list = container.find_elements(By.CSS_SELECTOR, ".info_box")
#
#         for car_tag in car_list:
#             link = car_tag.find_element(By.CSS_SELECTOR, "a:first-of-type")
#             href = link.get_attribute('href')
#             if href:
#                 url_list.append(href + '%20%EC%98%A4%EB%84%88%ED%8F%89%EA%B0%80')
#
#         next_button = driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[4]/div/a[2]')
#         next_button.click()
#         time.sleep(3)
#
#     except Exception as e:
#         print(f"오류 발생: {e}")
#
# # 최종 결과 출력
# print(f"총 수집된 링크 수: {len(url_list)}개")
# print(url_list)
#
# car_name_list = []
# avg_score_list = []
# count_ppl_list = []
# graph_data_list = []
# comments_data_list = []
#
#
# for url in url_list:
#     try:
#         driver.get(url)
#         time.sleep(3)
#
#         try:
#             # 차 이름
#             car_name = driver.find_element(By.CSS_SELECTOR, ".area_text_title")
#             car_name_list.append(car_name.text)
#         except:
#            car_name_list.append(None)
#
#         try:
#             # 평균 점수
#             avg_score = driver.find_element(By.CSS_SELECTOR, ".area_star_number._avg")
#             avg_score_list.append(avg_score.text)
#         except:
#             avg_score_list.append(None)
#
#         try:
#             # 설문 조사 작성한 사람들 수
#             count_ppl_text = driver.find_element(By.CSS_SELECTOR, '.area_people')
#             count_ppl_list.append(count_ppl_text.text)
#         except:
#             avg_score_list.append(None)
#
#         try:
#             # 그래프 데이터
#             graph_info = driver.find_elements(By.CSS_SELECTOR, '.guide._chart_label>li')
#             graph_data = []
#             for graph in graph_info:
#                 graph_data.append(graph.text)
#             graph_data_list.append(graph_data)
#         except:
#             avg_score_list.append(None)
#
#         try:
#             # 댓글 6개
#             comment_boxes = driver.find_elements(By.CLASS_NAME, 'u_cbox_comment_box')
#             comments = []
#             for box in comment_boxes[:6]:
#                 nickname = box.find_element(By.CLASS_NAME, 'u_cbox_nick').text
#                 average_rating = box.find_element(By.CLASS_NAME, 'u_cbox_multirating_totalcount_value').text
#                 # items = box.find_elements(By.CSS_SELECTOR, '.u_cbox_multirating_eachcount_item')
#                 # item_scores = []
#                 # for item in items:
#                 #     label = item.find_element(By.CLASS_NAME, 'u_cbox_multirating_eachcount_label').text
#                 #     value = item.find_element(By.CLASS_NAME, 'u_cbox_multirating_eachcount_value').text
#                 #     item_scores.append((label, value))
#                 comment_text = box.find_element(By.CLASS_NAME, 'u_cbox_contents').text
#                 date = box.find_element(By.CLASS_NAME, 'u_cbox_date').text
#
#                 comments.append({
#                     'nickname': nickname,
#                     'average_rating': average_rating,
#                     # 'item_scores': item_scores,
#                     'comment': comment_text,
#                     'date': date,
#                 })
#             comments_data_list.append(comments)
#         except:
#             avg_score_list.append(None)
#
#         print(f"총 수집한 차: {len(car_name_list)}개")
#         print(f"총 수집한 평균 점수: {len(avg_score_list)}개")
#         print(f"총 수집한 설문 인원 수: {len(count_ppl_list)}개")
#         print(f"총 수집한 그래프 데이터 수: {len(graph_data_list)}개")
#         print(f"총 수집한 댓글 데이터 수: {len(comments_data_list)}개")
#
#         print('----------------------평균점수----------------------------')
#         print(car_name_list)
#         print('----------------------평균점수----------------------------')
#         print(avg_score_list)
#         print('----------------------몇명이 했는지----------------------------')
#         print(count_ppl_list)
#         print('----------------------그래프----------------------------')
#         print(graph_data_list)
#         print('----------------------리뷰목록----------------------------')
#         print(comments_data_list)
#     except Exception as e:
#         print(f"{url} 에서 오류 발생: {e}")



# ------------------------------------------- 연습 ----------------------------------------------------

from DB.dto.car_review_dto import CarReviewDTO
from DB.dto.comment_info_dto import CommentDTO
from DB.dao.car_review_dao import CarReviewDAO
from DB.dao.comment_info_dao import CommentDAO

car_reviews = []
comments = []
car_review_dao = CarReviewDAO(db_connection)


url_list = ['https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bjg1&pkid=128&os=36782295&qvt=0&query=2026%20%EC%95%84%EB%B0%98%EB%96%BC%20%ED%95%98%EC%9D%B4%EB%B8%8C%EB%A6%AC%EB%93%9C%20%EC%98%A4%EB%84%88%ED%8F%89%EA%B0%80',]

for url in url_list:
    try:
        driver.get(url)
        time.sleep(3)

        try:
            # 차 이름
            car_name = driver.find_element(By.CSS_SELECTOR, ".area_text_title")

            # 평균 점수
            avg_score = driver.find_element(By.CSS_SELECTOR, ".area_star_number._avg")

            # 설문 조사 작성한 사람들 수
            count_ppl = driver.find_element(By.CSS_SELECTOR, '.area_people')
            def get_count_ppl(ppl_unformatted: str) -> int:
                ppl_formatted = "".join( c for c in ppl_unformatted if c.isdigit())
                return int(ppl_formatted)
            final_count_ppl = get_count_ppl(count_ppl.text)

            # 그래프 데이터
            graph_info = driver.find_elements(By.CSS_SELECTOR, '.guide._chart_label>li')
            graph_data = []
            for graph in graph_info:
                graph_data.append(graph.text)

            graph_data_text = ",".join(graph_data)

            # DTO 객체 생성
            car_review = CarReviewDTO(car_name.text, avg_score.text, final_count_ppl, graph_data_text)



            # CarReviewDAO 객체를 사용하여 DB에 저장
            if car_review:
                car_review_dao.insert_car_review(car_review)


        except:
                car_review = None

    #     try:
    #         # 댓글 6개
    #         comment_boxes = driver.find_elements(By.CLASS_NAME, 'u_cbox_comment_box')
    #         comments = []
    #         for box in comment_boxes[:6]:
    #             nickname = box.find_element(By.CLASS_NAME, 'u_cbox_nick').text
    #             average_rating = box.find_element(By.CLASS_NAME, 'u_cbox_multirating_totalcount_value').text
    #             # items = box.find_elements(By.CSS_SELECTOR, '.u_cbox_multirating_eachcount_item')
    #             # item_scores = []
    #             # for item in items:
    #             #     label = item.find_element(By.CLASS_NAME, 'u_cbox_multirating_eachcount_label').text
    #             #     value = item.find_element(By.CLASS_NAME, 'u_cbox_multirating_eachcount_value').text
    #             #     item_scores.append((label, value))
    #             comment_text = box.find_element(By.CLASS_NAME, 'u_cbox_contents').text
    #             date = box.find_element(By.CLASS_NAME, 'u_cbox_date').text
    #
    #             comments.append({
    #                 'nickname': nickname,
    #                 'average_rating': average_rating,
    #                 # 'item_scores': item_scores,
    #                 'comment': comment_text,
    #                 'date': date,
    #             })
    #         comments_data_list.append(comments)
    #     except:
    #         avg_score_list.append(None)
    #
    #     print(f"총 수집한 차: {len(car_name_list)}개")
    #     print(f"총 수집한 평균 점수: {len(avg_score_list)}개")
    #     print(f"총 수집한 설문 인원 수: {len(count_ppl_list)}개")
    #     print(f"총 수집한 그래프 데이터 수: {len(graph_data_list)}개")
    #     print(f"총 수집한 댓글 데이터 수: {len(comments_data_list)}개")
    #
    #     print('----------------------평균점수----------------------------')
    #     print(car_name_list)
    #     print('----------------------평균점수----------------------------')
    #     print(avg_score_list)
    #     print('----------------------몇명이 했는지----------------------------')
    #     print(count_ppl_list)
    #     print('----------------------그래프----------------------------')
    #     print(graph_data_list)
    #     print('----------------------리뷰목록----------------------------')
    #     print(comments_data_list)
    except Exception as e:
        print(f"{url} 에서 오류 발생: {e}")


