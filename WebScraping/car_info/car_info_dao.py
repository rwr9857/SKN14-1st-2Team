from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs
import re
import time
from WebScraping.car_info.car_info_dto import CarInfo
# from dto.car_info import CarInfo

class CarInfoDAO:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.car_info_list = []
        self.url_list = []

    def open_site(self):
        self.driver.get("https://naver.com")
        time.sleep(3)
        search_box = self.driver.find_element(By.ID, "query")
        search_box.send_keys("네이버 자동차")
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

    def apply_filters(self):
        button = self.driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[1]/div/div/div/ul/li[5]/div/a')
        button.click()
        time.sleep(2)

        slider = self.driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[1]/div/div/div/div/div/div/div[2]/div[1]/div[3]/div/span/span[7]')
        slider.click()
        time.sleep(2)

        actions = ActionChains(self.driver)
        for _ in range(2):
            actions.send_keys(Keys.ARROW_LEFT).perform()
        time.sleep(2)

        apply = self.driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/a')
        apply.click()
        time.sleep(2)

    def collect_urls(self):
        for page in range(1, 16):
            try:
                container = self.driver.find_element(By.XPATH, f'//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[3]/div[{page}]')
                car_list = container.find_elements(By.CSS_SELECTOR, ".info_box")

                for car_tag in car_list:
                    link = car_tag.find_element(By.CSS_SELECTOR, "a:first-of-type")
                    href = link.get_attribute('href')
                    if href and href not in self.url_list:
                        self.url_list.append(href + '%20%EC%A0%95%EB%B3%B4')

                next_button = self.driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[3]/div[2]/div[1]/div/div[4]/div/a[2]')
                next_button.click()
                time.sleep(3)

            except Exception as e:
                print(f"오류 발생 (페이지 {page}): {e}")
                break

    def _get_text_from_dd(self, info_groups, index):
        if len(info_groups) > index:
            dd_tag = info_groups[index].select_one('dd')
            return dd_tag.text.strip() if dd_tag else None
        return None

    def _extract_first_number(self, text, return_float=False):
        if not text:
            return None
        numbers = re.findall(r'\d+(?:\.\d+)?', text.replace(',', ''))
        if numbers:
            num = float(numbers[0])
            return round(num, 1) if return_float else int(num)
        return None

    def collect_car_info(self):
        for idx, url in enumerate(self.url_list, 1):
            try:
                self.driver.get(url)

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span.area_text_title strong._text'))
                )

                soup = bs(self.driver.page_source, 'html.parser')

                model_name_tag = soup.select_one('span.area_text_title strong._text')
                model_name = model_name_tag.text.strip() if model_name_tag else None

                sub_title_tags = soup.select('div.sub_title .txt')
                body_type = sub_title_tags[0].text.strip() if len(sub_title_tags) > 0 else None
                model_year = sub_title_tags[1].text.strip() if len(sub_title_tags) > 1 else None

                image_tag = soup.select_one('div.detail_info a.thumb.type_87_87 img')
                image_link = image_tag['src'] if image_tag else None

                info_groups = soup.select('dl.info .info_group')

                price_text = self._get_text_from_dd(info_groups, 0)
                price = self._extract_first_number(price_text)

                fuel_type = self._get_text_from_dd(info_groups, 1)

                fuel_efficiency_text = self._get_text_from_dd(info_groups, 2)
                fuel_efficiency = self._extract_first_number(fuel_efficiency_text, return_float=True)

                power_text = self._get_text_from_dd(info_groups, 3)
                power = self._extract_first_number(power_text)

                engine_type = None
                if len(info_groups) > 6:
                    engine_dd = info_groups[6].select_one('dd')
                    engine_span = info_groups[6].select_one('span.value_text')
                    engine_type = (engine_dd.text.strip() if engine_dd else '') + " " + (engine_span.text.strip() if engine_span else '')

                size = None
                size_text1 = self._get_text_from_dd(info_groups, 9)
                size_text2 = self._get_text_from_dd(info_groups, 12)
                if size_text1 and size_text2:
                    size_num1 = self._extract_first_number(size_text1)
                    size_num2 = self._extract_first_number(size_text2)
                    if size_num1 and size_num2:
                        size = round((size_num2 / size_num1) * 100, 2)

                brand = model_name.split()[0] if model_name else None

                if model_name:
                    car_info = CarInfo(
                        id=idx,
                        model_name=model_name,
                        body_type=body_type,
                        fuel_type=fuel_type,
                        price=price,
                        power=power,
                        fuel_efficiency=fuel_efficiency,
                        model_year=model_year,
                        size=size,
                        engine_type=engine_type,
                        image_link=image_link,
                        brand=brand
                    )
                    self.car_info_list.append(car_info)
                    print(f"[{idx}] {car_info}")
                else:
                    print(f"[{idx}] 모델명 없음")

            except TimeoutException:
                print(f"[{idx}] 타임아웃 발생: {url}")
            except Exception as e:
                print(f"[{idx}] 에러 발생: {e} URL: {url}")

    def quit(self):
        self.driver.quit()

    def get_car_info_list(self):
        return self.car_info_list
