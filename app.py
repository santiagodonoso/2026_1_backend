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
        user_pk = uuid.uuid4().hex
        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s)"        
        cursor.execute(q, (user_pk, user_first_name, user_last_name))
        db.commit()
        return "ok"
    except Exception as ex:
        print(ex, flush=True) # ('User first name minimum 2 characters', 400) # tuple
        return ex.args[0], ex.args[1]
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()









