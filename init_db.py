import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_tables():
    """
    Connects to the database and creates the necessary tables 
    (users and habits) if they do not exist.
    """
    
    # 1. Get the Database URL from the environment
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("Error: DATABASE_URL not found in .env file.")
        return

    try:
        print(" Connecting to the database...")
        conn = psycopg2.connect(url)
        cur = conn.cursor()

        # --- 2. CREATE USERS TABLE ---
        print("Creating 'users' table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                email VARCHAR(150) NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # --- 3. CREATE HABITS TABLE ---
        print("Creating 'habits' table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                streak INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Commit the changes to the database
        conn.commit()
        print("SUCCESS! All tables created successfully.")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f" Critical Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()