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

    print("\n✅ 최종 수집된 CarInfo 수:", len(dao.get_car_info_list()))

if __name__ == "__main__":
    main()