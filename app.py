from flask import Flask, request, jsonify
import json
import sqlite3
# print(__all__.doc)

app = Flask(__name__)


def db_connection():
    """
    Establish a connection with the database using SQLite3 
    """
    conn = None
    try:
        conn = sqlite3.connect("dbtable.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

@app.route("/users", methods=["GET", "POST"])
def users():
    """
    This is a data entry API, which get backs the inserted data and also
    used to insert new data to the database.

    Parameters
    ----------
    id : int
        The id tells the number of the entry which tells us the specific
        person in the database.

    name : str
        The name tells us the name of the person in the database.

    salary : float 
        The salary tells us about the salary of the people in th database.
    
    new_name : str
        If you want to add a new entry in the database 

    new_salary : float
        For the new entry you shoud give the new salary
    
    
    Response
    --------
        201 : The request was successful and as a result a resource has been created.

    """

    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor= conn.execute("SELECT * FROM Employees")
        dbtable= [
            dict(id=row[0], name=row[1], salary=row[2])
            for row in cursor.fetchall()
        ]
        if dbtable is not None:
            return jsonify(dbtable)
    if request.method == "POST":
        new_name = request.form["name"]
        new_salary = request.form["salary"]


    sql = """INSERT INTO Employees (name, salary)
                VALUES (?, ?) """
    cursor = cursor.execute(sql, (new_name, new_salary))
    conn.commit()
    return f"Employee with the id: {cursor.lastrowid} created successfully", 201



@app.route("/Employees/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_employee(id):

    """
    This will retreive, update and delete the database entries using the id of the entry.

    Parameters
    ----------
    id : int
        Used to give the id of the entry that you ant to update
        or delete.
    name : str
        The name tells us the updates name of the person in the database.

    salary : float 
        The salary tells us about the updated salary of the people in th database.
    

    Responses
    ---------
        200 : The request was received and understood and is being processed. 
        404 : The resource is missing 

    """
    conn = db_connection()
    cursor = conn.cursor()
    Employees = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM Employees WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
          Employees = r
        if Employees is not None:
            return jsonify(Employees), 200
        else:
            return "Something wrong", 404

    if request.method == "PUT":
        sql = """ UPDATE Employees SET name=?, salary=? WHERE id=? """
        name = request.form["name"]
        salary = request.form["salary"]
        
        updated_book = { 
            "id": id,
            "name": name,
            "salary": salary
                 }
        conn.execute(sql, (name, salary, id))
        conn.commit()
        return jsonify(updated_book)

    if request.method == "DELETE":
        sql = """ DELETE FROM Employees WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The employee with id: {} has been deleted.".format(id), 200



if __name__ == "__main__":
    app.run(debug=True)
