import mysql.connector



# Replace these with your own values
db_user = "test_user"
db_password = "pokemon123"
db_host = "34.132.140.184"  # You can find this in the Google Cloud Console
db_name = "concertfinderdb"
sql_script_file = "create_tables.sql"

def test_table():
    # Create a connection to the database
    connection = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )

    # Create a cursor to interact with the database
    cursor = connection.cursor()

    # Define the SQL statement to create a table
    create_table_query = """
    CREATE TABLE user_concerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    concert_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (concert_id) REFERENCES concerts(concert_id)
);


    
    """

    # Execute the SQL statement to create the table
    cursor.execute(create_table_query)

    # Commit the transaction
    connection.commit()

    # Close the cursor and the connection
    cursor.close()
    connection.close()


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
        print(connection)
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

def get_tables_from_db():
    conn= connection()
    cursor = conn.cursor()

# SQL query to retrieve a list of tables in your database
    show_tables_query = "SHOW TABLES"

    # Execute the query
    cursor.execute(show_tables_query)

    # Fetch all the rows (tables) from the result set
    tables = cursor.fetchall()
   
    # Print the list of tables
    for table in tables:
        print(table[0])

    # Close the cursor and the database connection
    cursor.close()
    conn.close()

def get_user_id(email):
    conn = connection()
    cursor = conn.cursor()

    # Use a parameterized query to prevent SQL injection
    table_query = "SELECT user_id FROM users WHERE email = %s"
    cursor.execute(table_query, (email,))

    result = cursor.fetchone()  # Use fetchone() to retrieve a single row
    user_id=result[0]
    cursor.close()
    conn.close()

    return user_id

def query_table(table_name):
    conn = connection()
    cursor = conn.cursor()
    table_query = f"SELECT * FROM {table_name}"
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

def delete_users_by_email(email):
    conn = connection()
    cursor = conn.cursor()

    # Delete users with the specified email
    delete_query = f"DELETE FROM users WHERE email = '{email}'"
    cursor.execute(delete_query)
    conn.commit()

    # Check if any rows were affected
    if cursor.rowcount > 0:
        print(f"Deleted {cursor.rowcount} user(s) with email {email}")
    else:
        print(f"No users found with email {email}")

    cursor.close()
    conn.close()

def delete_favorite_artist_by_id(user_id):
    conn = connection()
    cursor = conn.cursor()

    # Delete the favorite artist with the specified ID
    delete_query = f"DELETE FROM favorite_artists WHERE user_id = {user_id}"
    cursor.execute(delete_query)
    conn.commit()

    # Check if any rows were affected
    if cursor.rowcount > 0:
        print(f"Deleted favorite artist with ID {user_id}")
    else:
        print(f"No favorite artist found with ID {user_id}")

    cursor.close()
    conn.close()


def query_user_name(id):
    conn = connection()
    cursor = conn.cursor()
    user_name_query= f"SELECT username FROM users WHERE user_id = {id}"
    cursor.execute(user_name_query)
    result = cursor.fetchone()
    return result


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

def query_artists(email):
    conn = connection()
    cursor = conn.cursor()
    id = get_user_id(email)
    # Use a parameterized query to prevent SQL injection
    table_query = "SELECT artist_name FROM favorite_artists WHERE user_id = %s"
    cursor.execute(table_query, (id,))

    result = cursor.fetchall()  # Use fetchone() to retrieve a single row
    cursor.close()
    conn.close()
    return result

def query_artists_by_id(id):
    conn = connection()
    cursor = conn.cursor()
    table_query = "SELECT artist_name FROM favorite_artists WHERE user_id = %s"
    cursor.execute(table_query, (id,))

    result = cursor.fetchall()  # Use fetchone() to retrieve a single row
    cursor.close()
    conn.close()
    return result

def insert_users(username, email):
    conn = connection()
    cursor = conn.cursor()

    # Check if the email or username already exists
    check_query = f"SELECT * FROM users WHERE username = '{username}' OR email = '{email}'"
    cursor.execute(check_query)
    existing_user = cursor.fetchone()

    if existing_user:
        print("User with the same username or email already exists.")
    else:
        # Insert the user if not already in the database
        insert_query = f"INSERT INTO users (username, email) VALUES ('{username}', '{email}')"
        cursor.execute(insert_query)
        conn.commit()
        print('Successful insertion')

    cursor.close()
    conn.close()


def insert_your_artists(email,artists):
    id = get_user_id(email)
    print(id)
    conn = connection()
    cursor = conn.cursor()

    for artist in artists:
        # Check if the artist exists in the database
        check_query = f"SELECT COUNT(*) FROM favorite_artists WHERE user_id = '{id}' AND artist_name = '{artist}'"
        cursor.execute(check_query)
        result = cursor.fetchone()

        if result[0] == 0:
            # Artist does not exist, insert it
            insert_artist_query = f"INSERT INTO favorite_artists (user_id, artist_name) VALUES ('{id}', '{artist}')"
            cursor.execute(insert_artist_query)

    conn.commit()
    cursor.close()
    conn.close()
    print('successful insertion')

def users_w_similar_artists(email):
    current_user_id = get_user_id(email)
    conn = connection()
    cursor = conn.cursor()
    list_artists = query_artists(email)
   
    outer_id_similar={}
    for artist_tuple in list_artists:
        artist = artist_tuple[0]  # Unpack the value from the tuple
      
        artist_id_query = f"SELECT user_id FROM favorite_artists WHERE user_id != {current_user_id} and artist_name='{artist}'"
        cursor.execute(artist_id_query)
        result = cursor.fetchall()
        
        for id_ in result:
            id=id_[0]
            id=str(id)
            user_name=query_user_name(id)[0]
            result=f'{id},{user_name}'
            if result not in outer_id_similar:
                outer_id_similar[result]=[]

            outer_id_similar[result].append(artist)
        
    
    print(outer_id_similar)
    return outer_id_similar





# query_table('users')
# query_table('favorite_artists')





insert_users('testuser1', 'testuser1@gmail.com')
insert_your_artists('testuser1@gmail.com',['Drake','Bad Bunny','Mozart'])