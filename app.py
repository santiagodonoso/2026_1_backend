from flask import Flask, render_template, request, jsonify
import x
import uuid
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
        return render_template("page_signup.html")
    except Execption as ex:
        print(ex, flush = True)
        return "ups ..."

##############################
@app.post("/check-username")
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
        print(ex, flush = True)

        return f"""
            <browser mix-update="span">
                {ex.args[0]}
            </browser>
        """
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()  




