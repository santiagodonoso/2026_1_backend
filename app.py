from flask import Flask, render_template, request, jsonify
import x
import uuid
app = Flask(__name__)



##############################
@app.get("/")
def show_index():
    try:
        return render_template("page_index.html")
    except Exception as ex:
        return "system under maintenance ...", 500

##############################
@app.get("/items")
def show_items():
    try:
        db, cursor = x.db()
        q = "SELECT * FROM users"
        cursor.execute(q)
        users = cursor.fetchall()
        return render_template("items.html", users=users)
    except Exception as ex:
        print(ex, flush = True)
        return "system under maintenance ...", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()





##############################
"""
@app.get("/items")
def get_all_items():
    try:
        db, cursor = x.db()
        q = "SELECT * FROM users"
        cursor.execute(q)
        users = cursor.fetchall()
        return jsonify(users)
    except Exception as ex:
        print(ex, flush=True)
        return "ups ...", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()
"""

##############################
@app.get("/items/<id>")
def get_item_by_id(id):
    try:
        # Best case scenario
        # TODO: Validate the id
        # Connect to the database
        db, cursor = x.db()
        # Create a query
        q = "SELECT * FROM users WHERE user_pk = %s"
        # Execute the query. The second argument is a tuple
        # If the tuple only has 1 argument, then a comma after the argument
        cursor.execute(q, (id,))
        user = cursor.fetchone()
        return jsonify(user)
    except Exception as ex:
        # Worst case scenario
        print(ex, flush=True)
        return "ups ...", 500
    finally:
        # Runs after the try or after the except
        # In other words, it always runs
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



##############################
@app.post("/users")
def create_user():
    try:
        # TODO: Validate user_name
        # TODO: Validate user_last_name

        user_pk = uuid.uuid4().hex
        user_name = request.form.get("user_name")
        user_last_name = request.form.get("user_last_name")

        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s)"
        cursor.execute(q, (user_pk, user_name, user_last_name))
        db.commit()
        return jsonify({"id":user_pk}), 201
    except Exception as ex:
        pass
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
"""
@app.post("/users")
def create_user():
    try:
        # TODO: Validate user_name
        # TODO: Validate user_last_name

        user_pk = uuid.uuid4().hex
        user_name = request.form.get("user_name")
        user_last_name = request.form.get("user_last_name")

        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s)"
        cursor.execute(q, (user_pk, user_name, user_last_name))
        db.commit()
        return jsonify({"id":user_pk}), 201
    except Exception as ex:
        pass
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()
"""

##############################
@app.delete("/users/<user_pk>")
def delete_user(user_pk):
    try:
        # TODO: validate user_pk
        db, cursor = x.db()
        q = "DELETE FROM users WHERE user_pk = %s"
        cursor.execute(q, (user_pk,))
        db.commit()
        return f"""
            <browser mix-remove="#user-{user_pk}" mix-fade-2000>
            </browser>
        """
        #return "", 204
    except Exception as ex:
        pass
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.patch("/items/<id>")
def update_item(id):
    try:

        parts = []
        values = []

        user_name = request.form.get("user_name", "")
        user_name = user_name.strip()
        if user_name:
            parts.append("user_name = %s")
            values.append(user_name)

        user_last_name = request.form.get("user_last_name", "")
        user_last_name = user_last_name.strip()
        if user_last_name:
            parts.append("user_last_name = %s")
            values.append(user_last_name)

        if not user_name and not user_last_name: return "nothing to update", 400
        # Convert the list to a string with a comma in between
        partial_query = ", ".join(parts)

        values.append(id)

        print(parts, flush=True)
        print(values, flush=True)
        print(partial_query, flush=True)

        q = f"""
            UPDATE users
            SET	{partial_query}
            WHERE user_pk = %s
        """
        print(q, flush=True)

        db, cursor = x.db()
        cursor.execute(q, values)
        db.commit()
        return f"{user_name} {user_last_name}"


    except Exception as ex:
        print(ex)
        # Cast the exception to an string
        return str(ex), 500 # Internal server error
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()









