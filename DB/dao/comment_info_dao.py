import mysql.connector
from DB.dto.comment_info_dto import CommentDTO

class CommentDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_comments_by_review_id(self, review_id):
        query = "SELECT nickname, comment_avg_score, comment_text, created_at FROM comment_info WHERE review_id = %s"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (review_id,))
        result = cursor.fetchall()
        return [CommentDTO(review_id, *row) for row in result]

    def insert_comment(self, comment_dto):
        try:
            cursor = self.db_connection.cursor()
            query = """INSERT INTO comment_info (review_id, nickname, comment_avg_score, comment_text, created_at)
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                comment_dto.review_id,  # review_id를 사용하여 댓글과 리뷰를 연결
                comment_dto.nickname,
                comment_dto.comment_avg_score,
                comment_dto.comment_text,
                comment_dto.created_at
            ))
            self.db_connection.commit()

            # 마지막으로 삽입된 comment의 id를 DTO에 설정
            comment_dto.comment_id = cursor.lastrowid
        except Exception as e:
            print(f"Error while inserting comment: {e}")
        finally:
            cursor.close()