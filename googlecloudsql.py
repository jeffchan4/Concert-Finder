import mysql.connector



# Replace these with your own values
db_user = "test_user"
db_password = "pokemon123"
db_host = "34.132.140.184"  # You can find this in the Google Cloud Console
db_name = "concertfinderdb"
sql_script_file = "create_tables.sql"

def connection():
    connection = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )

    # No need to create a cursor here
    return connection

def createdb():
    try:
        connection = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )

        # Create a cursor to interact with the database
        cursor = connection.cursor()

        # Read and execute the SQL script file
        with open(sql_script_file, "r") as script_file:
            sql_script = script_file.read()
            cursor.execute(sql_script, multi=True)

        print("Tables created successfully!")

        # Commit the transaction
        connection.commit()

        # Close the cursor and the connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def query_table(table_name):
    conn = connection()
    cursor = conn.cursor()
    table_query = f"SELECT email FROM {table_name}"
    cursor.execute(table_query)
    result = cursor.fetchall()  # Use fetchall() to retrieve all rows

    for row in result:
        print(row)  # Print each row

    cursor.close()
    conn.close()

def delete_table(table_name):
    conn = connection()

    # Create a cursor to interact with the database
    cursor = conn.cursor()
    drop_table_query = f"DROP TABLE {table_name}"
    cursor.execute(drop_table_query)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Table '{table_name}' deleted successfully!")


def query_user(email):
    conn = connection()
    cursor = conn.cursor()

    # Use a parameterized query to prevent SQL injection
    table_query = "SELECT email FROM users WHERE email = %s"
    cursor.execute(table_query, (email,))

    result = cursor.fetchone()  # Use fetchone() to retrieve a single row
    cursor.close()
    conn.close()

    if result:
        return True
    return False


def insert_users(username, email):
    conn = connection()
    cursor = conn.cursor()
    insert_query = f"INSERT INTO users (username, email) VALUES ('{username}', '{email}')"
    cursor.execute(insert_query)
    conn.commit()
    cursor.close()
    conn.close()
    print('successful insertion')

def insert_your_artists(username,email,artists):
    conn = connection()
    cursor = conn.cursor()
    insert_query = f"INSERT INTO users (username, email) VALUES ('{username}', '{email}')"


query_user('testuser1@gmail.com')



