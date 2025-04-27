class CommentDTO:
    def __init__(self, review_id, nickname, comment_avg_score, comment_text, created_at):
        self.__review_id = review_id
        self.__nickname = nickname
        self.__comment_avg_score = comment_avg_score
        self.__comment_text = comment_text
        self.__created_at = created_at

    @property
    def review_id(self):
        return self.__review_id

    @review_id.setter
    def review_id(self, value):
        self.__review_id = value

    @property
    def nickname(self):
        return self.__nickname

    @nickname.setter
    def nickname(self, value):
        self.__nickname = value

    @property
    def comment_avg_score(self):
        return self.__comment_avg_score

    @comment_avg_score.setter
    def comment_avg_score(self, value):
        self.__comment_avg_score = value

    @property
    def comment_text(self):
        return self.__comment_text

    @comment_text.setter
    def comment_text(self, value):
        self.__comment_text = value

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, value):
        self.__created_at = value

    def __str__(self):
        return (f"CommentDTO(review_id={self.__review_id}, "
                f"nickname={self.__nickname}, "
                f"comment_avg_score={self.__comment_avg_score}, "
                f"comment_text={self.__comment_text}, "
                f"created_at={self.__created_at})")