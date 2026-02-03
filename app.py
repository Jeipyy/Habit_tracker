import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="habit_tracker",
        user="postgres",
        password="admin88"
    )

@app.route('/')
def home():
    conn = get_connection()
    cursor = conn.cursor()
    
    # SQL PRO: I fetch ID, Name, Description AND the completion count (total_done)
    query = """
        SELECT h.id, h.name, h.description, COUNT(l.id) as total_done
        FROM habits h
        LEFT JOIN logs l ON h.id = l.habit_id
        GROUP BY h.id, h.name, h.description
        ORDER BY h.id ASC;
    """
    
    cursor.execute(query)
    my_habits = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Now 'habit[3]' will hold the number of times completed (0, 1, 5, etc.)
    return render_template('index.html', habits=my_habits)

# CHANGE 2: New Route to handle the button click
@app.route('/complete', methods=['POST'])
def complete_habit():
    # request.form is like 'input()' but for web
    habit_id = request.form.get('habit_id') 
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # I insert into history (logs)
    cursor.execute("INSERT INTO logs (habit_id, is_completed) VALUES (%s, %s);", (habit_id, True))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    # When finished, I reload the main page (home)
    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
def add_habit():
    # 1. I receive the text from the input
    habit_name = request.form.get('habit_name')
    
    # 2. I connect and Save (Default description='...' and daily)
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO habits (user_id, name, description, goal_quantity, frequency_period)
        VALUES (1, %s, 'Creado desde la Web', 1, 'daily');
    """, (habit_name,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    # 3. I reload the page
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete_habit():
    habit_id = request.form.get('habit_id')
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # I delete logs (history) first to avoid Foreign Key errors
    cursor.execute("DELETE FROM logs WHERE habit_id = %s;", (habit_id,))
    # Then I delete the habit
    cursor.execute("DELETE FROM habits WHERE id = %s;", (habit_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('home'))    

if __name__ == '__main__':
    app.run(debug=True)