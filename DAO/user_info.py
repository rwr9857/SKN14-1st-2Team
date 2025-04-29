from DB.database import Database
import mysql.connector


class UserInfoDAO:
    def __init__(self):
        self.conn = Database().get_connection()

    def save_user_info(
        self, age: int, gender: str, job_id: int, purpose: str
    ) -> int | None:
        cursor = self.conn.cursor()
        try:
            query = """
                    INSERT INTO teamdb.user_info 
                    (USER_AGE, USER_GENDER, user_job, user_purpose)
                    VALUES (%s, %s, %s, %s)
                """
            values = (age, gender, job_id, purpose)

            cursor.execute(query, values)
            self.conn.commit()
            user_id = cursor.lastrowid

            return user_id
        except mysql.connector.Error as e:
            print(f"[ERROR] 사용자 정보 저장 실패: {e}")
            return None
        finally:
            cursor.close()
