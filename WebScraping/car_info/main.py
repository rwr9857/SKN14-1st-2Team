from WebScraping.car_info.car_info_dao import CarInfoDAO

def main():
    dao = CarInfoDAO()

    try:
        dao.open_site()
        dao.apply_filters()
        dao.collect_urls()
        dao.collect_car_info()

    finally:
        dao.quit()

    #print("\n✅ 최종 수집된 CarInfo 수:", len(dao.get_car_info_list()))

    # 크롤링 후 최종 수집된 데이터
    car_info_list = dao.get_car_info_list()

    # car_info_list 반환
    return car_info_list

if __name__ == "__main__":
    # 크롤링 데이터 저장
    car_info_list = main()

    # 저장된 데이터를 pickle로 저장
    import pickle
    with open('car_info_list.pkl', 'wb') as f:
        pickle.dump(car_info_list, f)

