import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- 1. DATABASE CONNECTION CONFIGURATION ---
def get_db_connection():
    # Attempt to get the secret URL from the Cloud Environment (Render)
    database_url = os.environ.get('DATABASE_URL')
    
    # Fallback: If running locally (no Env Var found), use my direct Neon link
    if database_url is None:
        database_url = "postgresql://neondb_owner:npg_JT6WL2nZIGdM@ep-little-haze-aiiwm676-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
    
    conn = psycopg2.connect(database_url)
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # I fetch all habits ordering them by ID so they don't jump around
    cur.execute('SELECT id, name, streak, completed_today FROM habits ORDER BY id ASC;')
    habits = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # Render the main HTML page passing the list of habits
    return render_template('index.html', habits=habits)

@app.route('/add', methods=['POST'])
def add_habit():
    # 1. Capture the text input from the form
    habit_name = request.form.get('habit_name')
    
    if habit_name:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 2. Insert the new habit (Streak starts at 0 by default in SQL)
        cur.execute("INSERT INTO habits (name) VALUES (%s)", (habit_name,))
        
        conn.commit()
        cur.close()
        conn.close()
        
    # 3. Refresh the page to show the new habit
    return redirect(url_for('home'))

@app.route('/complete', methods=['POST'])
def complete_habit():
    habit_id = request.form.get('habit_id')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Level up streak (+1) and mark 'completed_today' as True
    cur.execute("UPDATE habits SET streak = streak + 1, completed_today = TRUE WHERE id = %s", (habit_id,))
    
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete_habit():
    habit_id = request.form.get('habit_id')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Remove the row from the database permanently
    cur.execute('DELETE FROM habits WHERE id = %s', (habit_id,))
    
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('home'))

@app.route('/reset', methods=['POST'])
def reset_day():
    # DEBUG TOOL: A hidden button to reset the day (sets all 'completed_today' to False)
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("UPDATE habits SET completed_today = FALSE")
    
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Cloud Config: Get the PORT from the environment, default to 5000 if local
    port = int(os.environ.get("PORT", 5000))
    # '0.0.0.0' is required for the server to be accessible externally
    app.run(host='0.0.0.0', port=port, debug=True)