from flask import request
import mysql.connector

##############################
def db():
    try:
        db = mysql.connector.connect(
            host = "mariadb",
            user = "root",  
            password = "password",
            database = "2026_1_backend"
        )
        cursor = db.cursor(dictionary=True)
        return db, cursor
    except Exception as e:
        print(e, flush=True)
        raise Exception("Database under maintenance", 500)


##############################
USER_FIRST_NAME_MIN = 2
USER_FIRST_NAME_MAX = 20
def validate_user_first_name():
    user_first_name = request.form.get("user_first_name", "").strip()
    if len(user_first_name) < USER_FIRST_NAME_MIN:
        raise Exception(f"User first name minimum {USER_FIRST_NAME_MIN } characters", 400)
    if len(user_first_name) > USER_FIRST_NAME_MAX:
        raise Exception(f"User first name maximum {USER_FIRST_NAME_MAX } characters", 400)    
    return user_first_name










