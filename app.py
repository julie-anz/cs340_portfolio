""" 
The code on this page is an adaptation of the code found on the following CS340 Canvas Pages:
    - Web Application Technology: https://canvas.oregonstate.edu/courses/2017561/pages/exploration-web-application-technology-2?module_item_id=25645131
    - Implementing CUD operations in your app: https://canvas.oregonstate.edu/courses/2017561/pages/exploration-implementing-cud-operations-in-your-app?module_item_id=25645149
"""

# ########################################
# ########## SETUP

from flask import Flask, render_template, request, redirect, flash
from database.db_connector import *
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()


# Database credentials
host = 'classmysql.engr.oregonstate.edu'    
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
db = os.getenv("MYSQL_DB")

PORT = os.getenv("MY_PORT")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'default-secret-key' #needed for flash messages

# ########################################
# ########## ROUTE HANDLERS

# READ ROUTES
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and request.form.get("reset-form") == "reset":
        try:
            reset()
            return redirect("/") 
        except Exception as e:
            flash(f"An error occurred resetting the database. {e}", 'error')
            return redirect("/")

    else:
        try:
            return render_template("home.j2", action_name="'/'")

        except Exception as e:
            flash(f"An error occurred while rendering the page. {e}", 'error')
            return render_template('home.j2', action_name="'/'")

@app.route("/users", methods=['GET', 'POST'])
def users():
    
    if request.method == 'POST' and request.form.get("reset-form") == "reset":
        try:
            reset()
            return redirect("/users")
        except Exception as e:
            flash(f"An error occurred resetting the database. {e}", 'error')
            return redirect("/users")

    dbConnection = connectDB(host, user, password, db)  # Open our database connection

    heading = "On this page you can view records in the Users table."
    try:
        # Create and execute our query
        query1 = "SELECT * FROM Users;"
        users = query(dbConnection, query1).fetchall()
        headers = ["First Name", "Last Name", "Email", "Phone", "Delete"]

        # Render the users.j2 file, and also send the renderer an object containing the users information
        return render_template(
            "users.j2", headers=headers, users=users, heading=heading, action_name="'/users'"
        )
    
    except Exception as e:
        flash(f"An error occurred while executing the database queries. {e}",'error')
        return render_template(
            "users.j2", headers=headers, users=users, heading=heading, action_name="'/users'"
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

@app.route("/loans", methods=['GET', 'POST'])
def loans(): 
    
    if request.method == 'POST' and request.form.get("reset-form") == "reset":
        try:
            reset()
            return redirect("/loans")
        except Exception as e:
            flash(f"An error occurred resetting the database. {e}", 'error')
            return redirect("/loans")

    dbConnection = connectDB(host, user, password, db)  # Open our database connection

    heading = "On this page you can view and delete records in the Loans table."
    try:
        # Create and execute our query
        query1 = "SELECT l.loanID, l.startDate, l.dueDate, r.resourceName, u.firstName, u.lastName FROM Loans l JOIN Users u on l.userID = u.userID JOIN Resources r on l.resourceID = r.resourceID;"
     
        loans = query(dbConnection, query1).fetchall()
        headers = ["Start Date", "Due Date", "Resource Name", "Borrower First Name", "Borrower Last Name", "Delete"]

        userQuery = "SELECT userID, CONCAT(firstName, ' ', lastName) AS name FROM Users;"
        users = query(dbConnection, userQuery).fetchall()

        resourceQuery = "SELECT resourceID, resourceName, resourceDescription FROM Resources;"
        resources = query(dbConnection, resourceQuery).fetchall()

        # Render the loans.j2 file, and also send the renderer an object containing the loan's information
        return render_template(
            "loans.j2", headers=headers, loans=loans, heading=heading, users=users, resources=resources, action_name="'/loans'"
        )
    
    except Exception as e:
        flash(f"An error occurred while executing the database queries. {e}",'error')
        return render_template(
            "loans.j2", headers=headers, loans=loans, heading=heading, users=users, resources=resources, action_name="'/loans'"
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


@app.route("/resources", methods=['GET','POST'])
def resources():
    
    if request.method == 'POST' and request.form.get("reset-form") == "reset":
        try:
            reset()
            return redirect("/resources")
        except Exception as e:
            flash(f"An error occurred resetting the database. {e}", 'error')
            return redirect("/resources")

    dbConnection = connectDB(host, user, password, db)  # Open our database connection

    heading = "On this page you can view and delete records in the Resources table."
    try:
        # Create and execute our query
        query1 = "SELECT r.resourceID, r.resourceName, r.resourceDescription, u.firstName, u.lastName FROM Resources r JOIN Users u on r.userID = u.userID ;"
     
        resources = query(dbConnection, query1).fetchall()
        headers = ["Resource Name", "Resource Description", "Owner First Name", "Owner Last Name", "Delete"]

        userQuery = "SELECT userID, CONCAT(firstName, ' ', lastName) AS name FROM Users;"
        users = query(dbConnection, userQuery).fetchall()

        # Render the resources.j2 file, and also send the renderer an object containing the resource's information
        return render_template(
            "resources.j2", headers=headers, resources=resources, heading=heading, users=users, action_name="'/resources'"
        )
    
    except Exception as e:
        flash(f"An error occurred while executing the database queries. {e}",'error' )
        return render_template(
            "resources.j2", headers=headers, resources=resources, heading=heading, users=users, action_name="'/resources'"
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

@app.route("/resourceLocations", methods=['GET','POST'])
def resourceLocations():
    
    if request.method == 'POST' and request.form.get("reset-form") == "reset":
        try:
            reset()
            return redirect("/resourceLocations")
        except Exception as e:
            flash(f"An error occurred resetting the database. {e}", 'error') 
            return redirect("/resourceLocations")

    dbConnection = connectDB(host, user, password, db)  # Open our database connection

    heading = "On this page you can view and delete records in the ResourceLocations table."

    try:
        # Create and execute our query
        query1 = "SELECT rl.resourceLocationsID, r.resourceName, l.locationName FROM ResourceLocations rl JOIN Resources r on rl.resourceID = r.resourceID JOIN Locations l on rl.locationID = l.locationID;"
     
        resourceLocations = query(dbConnection, query1).fetchall()
        headers = ["Resource Name", "Location Name", "Delete"]

        resourceQuery = "SELECT resourceID as id, resourceName AS name FROM Resources;"
        resources = query(dbConnection, resourceQuery).fetchall()

        locationQuery = "SELECT locationID as id, locationName AS name FROM Locations;"
        locations = query(dbConnection, locationQuery).fetchall()

        # Render the resourceLocations.j2 file, and also send the renderer an object containing the resourceLocation's information
        return render_template(
            "resourceLocations.j2", headers=headers, resourceLocations=resourceLocations, heading=heading, resources=resources, locations=locations, action_name="'/resourceLocations'"
        )
    
    except Exception as e:
        flash(f"An error occurred while executing the database queries. {e}", 'error')
        return render_template(
            "resourceLocations.j2", headers=headers, resourceLocations=resourceLocations, heading=heading, resources=resources, locations=locations, action_name="'/resourceLocations'"
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

@app.route("/locations", methods=['GET','POST'])
def locations():

    if request.method == 'POST' and request.form.get("reset-form") == "reset":
        try:
            reset()
            return redirect("/locations")
        except Exception as e:
            flash(f"An error occurred resetting the database. {e}", 'error') 
            return redirect("/locations")

    dbConnection = connectDB(host, user, password, db)  # Open our database connection

    heading = "On this page you can view and delete records in the Locations table."

    try:
        # Create and execute our query
        query1 = "SELECT * FROM Locations;"
     
        locations = query(dbConnection, query1).fetchall()
        headers = ["Location Name", "Location Description", "Delete"]

        # Render the locations.j2 file, and also send the renderer an object containing the location's information
        return render_template(
            "locations.j2", headers=headers, locations=locations, heading=heading, action_name="'/locations'"
        )
    
    except Exception as e:
        flash("An error occurred while executing the database queries. {e}", 'error')
        return render_template(
            "locations.j2", headers=headers, locations=locations, heading=heading, action_name="'/locations'"
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


@app.route("/delete", methods=['POST'])
def delete():
    """
    deletes a row from a specified table by ID
    """

    dbConnection = connectDB(host, user, password, db)  # Open our database connection

    table = request.form["table"]
    id = request.form["id"]
    name = request.form["name"]

    try:
        cursor = dbConnection.cursor()

        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query = f"CALL sp_delete_{table[:-1]}(%s);"
        cursor.execute(query, (id,))

        dbConnection.commit()  # commit the transaction

        # Redirect the user to the updated webpage
        return redirect(f"/{table}")

    except Exception as e:
        flash(f"An error occurred while executing the database queries. {e}", 'error')
        return redirect(f"/{table}")

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

@app.route("/update", methods=['POST'])
def update():
    """
    updates a single column in row from a specified table by ID
    """
    dbConnection = connectDB(host, user, password, db)  # Open our database connection
    
    table = request.form["table"]
    id = request.form.get("update_id")
    updateData = request.form.get("update_data")
    
    try:
        cursor = dbConnection.cursor()
   
        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query = f"CALL sp_update_{table[:-1]}(%s,%s);"
        cursor.execute(query,(id, updateData))
        
        dbConnection.commit()  # commit the transaction

        # Redirect the user to the updated webpage
        return redirect(f"/{table}")
    
    except Exception as e:
        flash(f"An error occurred while executing the database queries. {e}", 'error')
        return redirect(f"/{table}")
    
    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

@app.route("/create", methods=['POST'])
def create():
    """
    creates a new row in a specified table
    """

    table = request.form["table"]
   
    if table == "resources":
        userId = request.form.get("create_owner")
        name = request.form.get("create_resource_name")
        description = request.form.get("create_resource_description")
        return create_resource(table, userId, name, description)
    if table == "resourceLocations": 
        resourceId = request.form.get("create_resource")
        locationId = request.form.get("create_location")
        return create_resource_location(table, resourceId, locationId)
    if table == "users":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        phone = request.form.get("phone")
        email = request.form.get("user_email")
        return create_user(table, fname, lname, email, phone)
    if table == "locations":
        name = request.form.get("create_name")
        description = request.form.get("create_descr")
        return create_location(table, name, description)
    if table == "loans":
        sdate = request.form.get("sdate")
        ddate = request.form.get("ddate")
        userId = request.form.get("loan_user")
        resourceId = request.form.get("loan_resource")
        return create_loan(table, sdate, ddate, userId, resourceId)
    
###   
### # helper functions for insert operations
####
def create_resource(table, userId, name, description):
    dbConnection = connectDB(host, user, password, db)  # Open our database connection
    try:
        cursor = dbConnection.cursor()
   
        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query = f"CALL sp_insert_{table[:-1]}(%s,%s, %s);"
        cursor.execute(query,(userId, name, description))
        
        dbConnection.commit()  # commit the transaction

        # Redirect the user to the updated webpage
        return redirect(f"/{table}")
    
    except Exception as e:
        flash(f"An error occurred while executing the database queries. {e}", 'error')
        return redirect(f"/{table}")
    
    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


def create_resource_location(table, resourceId, locationId):
    dbConnection = connectDB(host, user, password, db)  # Open our database connection
    try:
        cursor = dbConnection.cursor()
   
        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query = f"CALL sp_insert_{table[:-1]}(%s,%s);"
        cursor.execute(query,(resourceId, locationId))
        
        dbConnection.commit()  # commit the transaction

        # Redirect the user to the updated webpage
        return redirect(f"/{table}")
    
    except Exception as e:
        flash(f"An error occurred while executing the database queries. {e}", 'error')
        return redirect(f"/{table}")
    
    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

def create_user(table, fname, lname, email, phone):
    dbConnection = connectDB(host, user, password, db)  # Open our database connection
    try:
        cursor = dbConnection.cursor()
   
        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query = f"CALL sp_insert_{table[:-1]}(%s,%s, %s, %s);"
        cursor.execute(query,(fname, lname, email, phone))
        
        dbConnection.commit()  # commit the transaction

        # Redirect the user to the updated webpage
        return redirect(f"/{table}")
    
    except Exception as e:
        flash(f"An error occurred while executing the database queries. {e}", 'error')
        return redirect(f"/{table}")
    
    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

def create_location(table, name, description):
    dbConnection = connectDB(host, user, password, db)  # Open our database connection
    try:
        cursor = dbConnection.cursor()
   
        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query = f"CALL sp_insert_{table[:-1]}(%s,%s);"
        cursor.execute(query,(name, description))
        
        dbConnection.commit()  # commit the transaction

        # Redirect the user to the updated webpage
        return redirect(f"/{table}")
    
    except Exception as e:
        flash(f"An error occurred while executing the database queries. {e}", 'error')
        return redirect(f"/{table}")
    
    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

def create_loan(table, sdate, ddate, userId, resourceId):
    dbConnection = connectDB(host, user, password, db)  # Open our database connection
    try:
        cursor = dbConnection.cursor()
   
        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query = f"CALL sp_insert_{table[:-1]}(%s,%s, %s, %s);"
        cursor.execute(query,(sdate, ddate, userId, resourceId))
        
        dbConnection.commit()  # commit the transaction

        # Redirect the user to the updated webpage
        return redirect(f"/{table}")
    
    except Exception as e:
        flash(f"An error occurred while executing the database queries. {e}", 'error')
        return redirect(f"/{table}")
    
    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


def reset():
    """
    Resets to starter tables / starter info.
    """
    dbConnection = connectDB(host, user, password, db)  # Open our database connection
    cursor = dbConnection.cursor()

    # Create and execute our queries
    # Using parameterized queries (Prevents SQL injection attacks)
    query = "CALL sp_reset();"
    cursor.execute(query,)
    dbConnection.commit()  # commit the transaction
    
    # Close the DB connection, if it exists
    if "dbConnection" in locals() and dbConnection:
        dbConnection.close()

# ########################################
# ########## LISTENER

if __name__ == "__main__":
    app.run(port=PORT, debug=True)
