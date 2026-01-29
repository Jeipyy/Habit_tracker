import psycopg2

def get_connection():
    """Helper function to get DB connection."""
    return psycopg2.connect(
        host="localhost",
        database="habit_tracker",
        user="postgres",
        password="admin88"
    )

def show_users():
    """Fetches and displays users from the DB."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, email FROM users;")
        users = cursor.fetchall()
        
        print("\n--- User List ---")
        for user in users:
            print(f"ID: {user[0]} | Username: {user[1]} | Email: {user[2]}")
        print("-----------------\n")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error fetching users: {e}")

def add_habit_log(): 
    """Asks user for input and saves it to DB."""
    print("\n--- Log New Habit ---")
    habit_id = input("Enter Habit ID to complete (e.g., 1): ")
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "INSERT INTO logs (habit_id, is_completed) VALUES (%s, %s);"
        
        data = (habit_id, True)
        
        cursor.execute(query, data)
        conn.commit() # Important: Save changes!
        
        print("\n Habit marked as completed.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f" Error saving data: {e}")

def main_menu():
    """Main loop for the application."""
    print("--- Starting Habit Tracker Core ---")
    
    while True:
        print("1. Show Users")
        print("2. Log Habit")
        print("3. Exit")
        
        choice = input("\nChoose option: ")

        if choice == "1":
            show_users()
        elif choice == "2":
            add_habit_log()
        elif choice == "3":
            print("Closing connection... Bye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main_menu()