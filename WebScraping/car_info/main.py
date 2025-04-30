import pickle
from WebScraping.car_info.car_crawler import CarCrawler


if __name__ == "__main__":
    car_crawler = CarCrawler()

    car_crawler.open_site()
    car_crawler.apply_filters()
    car_crawler.collect_urls()
    car_crawler.collect_car_info()

    car_crawler.quit()

    # print("\n✅ 최종 수집된 CarInfo 수:", len(car_crawler.get_car_info_list()))

    # 크롤링 후 최종 수집된 데이터
    car_info_list = car_crawler.get_car_info_list()

    with open("car_info_list.pkl", "wb") as f:
        pickle.dump(car_info_list, f)
