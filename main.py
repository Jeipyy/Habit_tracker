import psycopg2

def get_valid_id(prompt):
    """Loop until user enters a valid integer ID."""
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            return int(user_input)
        else:
            print("Error: You must enter a valid integer number. Try again.")


def get_connection():
    """Helper function to get DB connection."""
    return psycopg2.connect(
        host="localhost",
        database="habit_tracker",
        user="postgres",
        password="admin88"
    )

def create_habit():
    """Allows user to create a new habit from the console."""
    print("\n--- Create New Habit ---")

    name = input("Habit Name (Example. Gym): ")
    desc = input("Description (Example., 1 hour workout): ")
    
    goal = get_valid_id("Goal Quantity (times per period Example., 1): ")

    freq = input("Frequency (daily/weekly): ")

    if freq.lower() not in ['daily', 'weekly']:
        print(" Frequency set to default: 'daily'")
        freq = 'daily'

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO HABITS
            (user_id, name, description, goal_quantity, frequency_period)
            VALUES (1, %s, %s, %s, %s);
        """

        cursor.execute(query, (name, desc, goal, freq))
        conn.commit()

        print(f"\n Success! Habit '{name}' created. ")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating habit: {e} ")

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

    show_habits() #show habits before 

    habit_id = get_valid_id("Enter Habit ID to complete (e.g., 1): ")
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "INSERT INTO logs (habit_id, is_completed) VALUES (%s, %s);"
        
        data = (habit_id, True)
        
        cursor.execute(query, data)
        conn.commit() 
        
        print("\n Habit marked as completed.")
        print("\n-----------------------------")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f" Error saving data: {e}")

def show_habits():
    """Fetches and displays all habits."""

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description FROM habits;")
        habits = cursor.fetchall()

        print ("\n--- Active habits ---")
        for h in habits:
            print (f"ID: {h[0]} | Name: {h[1]} | Desc: {h[2]}")
        print("--------------------\n")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error fetching habits: {e}")


def delete_habit():
    """Deletes a habit from DB."""
    print("\n--- DELETE HABIT ---")

    show_habits()

    habit_id = get_valid_id("Enter habit ID to delete: ")

    confirm = input(f"Are you sure want to delete ID {habit_id}? (yes/no): ")

    if confirm.lower() == "yes":
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = "DELETE FROM habits WHERE id = %s;"

            cursor.execute(query, (habit_id,))
            conn.commit()

            if cursor.rowcount > 0:
                print(f"\n Habit {habit_id} deleted succesfully.")
            else:
                print(f"\n Habit {habit_id} not found.")

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error deleting: {e}")
    else:
        print("Operation cancelled.")

def view_history():
    """Shows a log of all completed habits using SQL JOIN."""
    print("\n--- History log ---")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT h.name, l.completed_at
        FROM logs l
        JOIN habits h ON l.habit_id = h.id
        ORDER BY l.completed_at DESC;
        """
        
        cursor.execute(query)
        history = cursor.fetchall()

        if not history:
            print("No history found. Start tracking habits!")
        else:
            for entry in history:
                print(f"completed {entry[0]} | Date: {entry[1]}")

        print("---------------------\n")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print (f"Error fetching history: {e}")

def main_menu():
    """Main loop for the application."""
    print("--- Starting Habit Tracker Core ---")
    
    while True:
        print("1. Show Users")
        print("2. Create New Habit")
        print("3. Log Habit (Mark as Done)")
        print("4. Delete a habit")
        print("5. View History")
        print("6. Exit")
        
        choice = input("\nChoose option: ")

        if choice == "1":
            show_users()
        elif choice == "2":
            create_habit()
        elif choice == "3":
            add_habit_log()
        elif choice == "4":
            delete_habit()
        elif choice == "5": 
            view_history()
        elif choice == "6":
            print("Closing connection!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main_menu()