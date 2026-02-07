import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# Import to load environment variables from .env file
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()

app = Flask(__name__)

# --- APP CONFIGURATION ---
# Security: Get the SECRET_KEY from environment variables. 
# It is crucial for signing session cookies.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')

# --- FLASK-LOGIN SETUP ---
login_manager = LoginManager()
login_manager.init_app(app)
# Redirect users to 'login' view if they try to access a protected page without authentication
login_manager.login_view = 'login' 

# --- DATABASE CONNECTION ---
def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.
    It fetches the URL securely from environment variables.
    """
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        raise ValueError("Critical Error: DATABASE_URL not found in .env file.")
    
    conn = psycopg2.connect(database_url)
    return conn

# --- USER MODEL ---
class User(UserMixin):
    """
    User class to handle Flask-Login session management.
    Inherits from UserMixin to get default methods like is_authenticated().
    """
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        """Fetches a single user by their ID from the database."""
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, username, email, password_hash FROM users WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                return User(id=user_data[0], username=user_data[1], email=user_data[2], password_hash=user_data[3])
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_username(username):
        """Fetches a user by their username (used during login)."""
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, username, email, password_hash FROM users WHERE username = %s", (username,))
            user_data = cur.fetchone()
            if user_data:
                return User(id=user_data[0], username=user_data[1], email=user_data[2], password_hash=user_data[3])
            return None
        finally:
            cur.close()
            conn.close()

# Flask-Login callback to load the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# --- ROUTES ---

@app.route('/')
@login_required # Security: Protects this route. Only logged-in users can access.
def home():
    """
    Main dashboard. 
    Displays the habits list associated with the current logged-in user.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Query: Select habits that belong specifically to the current user (current_user.id)
    cur.execute('SELECT id, name, description, streak FROM habits WHERE user_id = %s ORDER BY id ASC;', (current_user.id,))
    habits = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # Render the template passing the habits list and the user info
    return render_template('index.html', habits=habits, user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user authentication (Login)."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 1. Retrieve the user from the database
        user = User.get_by_username(username)
        
        # 2. Verify if user exists AND if the password hash matches
        if user and check_password_hash(user.password_hash, password):
            login_user(user) # Create session
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles new user registration."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Security: Hash the password using PBKDF2 (never store plain text passwords)
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # Insert new user into the database
            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            conn.commit()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback() # Rollback transaction in case of error (e.g., duplicate email)
            flash(f'Error creating account: {e}', 'danger')
        finally:
            cur.close()
            conn.close()
            
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Logs the user out and clears the session."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# --- HABIT MANAGEMENT ROUTES ---

@app.route('/add', methods=['POST'])
@login_required
def add_habit():
    """Creates a new habit linked to the authenticated user."""
    habit_name = request.form.get('habit_name')
    
    if habit_name:
        conn = get_db_connection()
        cur = conn.cursor()
        # SQL Insert: Associate the new habit with current_user.id
        cur.execute("INSERT INTO habits (name, user_id, streak) VALUES (%s, %s, 0)", (habit_name, current_user.id))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
@login_required
def delete_habit():
    """Deletes a habit (only if it belongs to the current user)."""
    habit_id = request.form.get('habit_id')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Security: Ensure users can only delete their own habits
    cur.execute('DELETE FROM habits WHERE id = %s AND user_id = %s', (habit_id, current_user.id))
    
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('home'))

@app.route('/complete', methods=['POST'])
@login_required
def complete_habit():
    """Marks a habit as completed and increases the streak."""
    habit_id = request.form.get('habit_id')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Update logic: Increase streak +1
    cur.execute("UPDATE habits SET streak = streak + 1 WHERE id = %s AND user_id = %s", (habit_id, current_user.id))
    
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Cloud Config: Get PORT from environment or default to 5000 for local development
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)