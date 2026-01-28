import psycopg2

def connect_to_database():
    """Establish a connection to the PostgreSQL database."""
    print("--- Starting Habit Tracker core ---")
    
    try:
        # Connection parameters
        connection = psycopg2.connect(
            host="localhost",
            database="habit_tracker",
            user="postgres",
            password="admin88" 
        )

        # If we reach this point, the connection was successful
        print(" System successfully linked to PostgreSQL.")
        
        # --- START QUERY BLOCK ---
        cursor = connection.cursor()
        
        # Execute the query 
        cursor.execute("SELECT id, username, email FROM users;")
        
        # Fetch all results
        users = cursor.fetchall()
        
        # Print results simply
        print("\n--- User List ---")
        for user in users:
            print(f"ID: {user[0]} | Username: {user[1]} | Email: {user[2]}")
        print("-----------------\n")
        
        cursor.close()
        # --- END QUERY BLOCK ---

        # Always close the connection
        connection.close()
        print("--- Connection closed safely ---")

    except Exception as error:
        print(f" Could not connect to database: {error}")

if __name__ == "__main__":
    connect_to_database()