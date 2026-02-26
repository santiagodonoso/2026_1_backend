from flask import Flask, render_template, request, jsonify
import x
import uuid
import time

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)


##############################
@app.post("/signup")
def signup():
    try:
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_username = x.validate_user_username()
        user_pk = uuid.uuid4().hex
        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s, %s)"        
        cursor.execute(q, (user_pk, user_first_name, user_last_name, user_username))
        db.commit()
        return "ok"
    except Exception as ex:

        # How do you check if it is a number
        if "Duplicate entry" in str(ex) and "user_username" in str(ex):
            return "username already in the system", 400

        return ex.args[0], ex.args[1]

        """
        try:
            # 1062 (23000): Duplicate entry 'santi' for key 'user_username'
            print(f"*********** {ex}", flush=True) # ('User first name minimum 2 characters', 400) # tuple
            print(f"0: {ex.args[0]}", flush=True) # 1062
            print(f"1: {ex.args[1]}", flush=True) # 1062 (23000): Duplicate entry 'santi' for key 'user_username'
            return ex.args[0], ex.args[1]
        except Exception as e:
            return "############# ups ###################"
            print(e, flush=True)
            if "Duplicate entry" in str(e) and "user_username" in str(e):
                return "user_username already exists", 400
        """



    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/signup")
def show_signup():
    try:
        return render_template("page_signup.html", x=x)
    except Exception as ex:
        print(ex, flush = True)
        return "ups ..."

##############################
@app.post("/api-check-username")
def check_username():
    try:
        user_username = x.validate_user_username()
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_username = %s"
        cursor.execute(q, (user_username,))
        row = cursor.fetchone()
        if not row:
            return f"""
                <browser mix-update="span">
                    Username available
                </browser>
            """
        
        return f"""
            <browser mix-update="span">
                Username taken
            </browser>
        """        


    except Exception as ex:
        # print(ex, flush = True)
        ic(ex)

        if "--error-- user_username" in str(ex):
            return f"""<browser mix-update="span">{ex.args[0]}</browser>""", 400

        # Worst case, something unexpected
        return f"""<browser mix-update="span">System under maintenance</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()  



##############################
@app.post("/api-create-user")
def create_user():
    try:
        user_username = x.validate_user_username()
        user_first_name = x.validate_user_first_name()
        user_pk = uuid.uuid4().hex
        user_create_at = int(time.time())
        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s, %s)"
        cursor.execute(q, (user_pk, user_username, user_first_name, user_create_at))
        db.commit()

        return """
        <browser mix-update="span">User created</browser>
        """
        
    

    except Exception as ex:
        # print(ex, flush = True)
        ic(ex)

        if "--error-- user_username" in str(ex):
            return f"""<browser mix-update="span">{ex.args[0]}</browser>""", 400

        if "--error-- user_first_name" in str(ex):
            return f"""<browser mix-update="span">{ex.args[0]}</browser>""", 400

        if "Duplicate entry" in str(ex) and "user_username" in str(ex):
            return f"""<browser mix-update="span">Username taken</browser>""", 400

        # Worst case, something unexpected
        return f"""<browser mix-update="span">System under maintenance</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()  
