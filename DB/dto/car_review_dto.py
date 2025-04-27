class CarReviewDTO:
    def __init__(self, car_name, avg_score, survey_people_count, graph_info):
        self.__car_name = car_name
        self.__avg_score = avg_score
        self.__survey_people_count = survey_people_count
        self.__graph_info = graph_info

    @property
    def car_name(self):
        return self.__car_name

    @car_name.setter
    def car_name(self, value):
        self.__car_name = value

    @property
    def avg_score(self):
        return self.__avg_score

    @avg_score.setter
    def avg_score(self, value):
        self.__avg_score = value

    @property
    def survey_people_count(self):
        return self.__survey_people_count

    @survey_people_count.setter
    def survey_people_count(self, value):
        self.__survey_people_count = value

    @property
    def graph_info(self):
        return self.__graph_info

    @graph_info.setter
    def graph_info(self, value):
        self.__graph_info = value

    def __str__(self):
        return (f"CarReviewDTO(car_name={self.__car_name}, "
                f"avg_score={self.__avg_score}, "
                f"survey_people_count={self.__survey_people_count}, "
                f"graph_info={self.__graph_info})")
