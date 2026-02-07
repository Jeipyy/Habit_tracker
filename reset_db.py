import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def reset_database():
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("❌ Error: No DATABASE_URL found.")
        return

    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()

        print("Deleting old tables (Cleaning up)...")
        # El CASCADE es importante: borra 'users' y todo lo que dependa de él (como habits)
        cur.execute("DROP TABLE IF EXISTS habits CASCADE;")
        cur.execute("DROP TABLE IF EXISTS users CASCADE;")
        
        print("🔨 Creating new 'users' table...")
        cur.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                email VARCHAR(150) NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        print("🔨 Creating new 'habits' table...")
        cur.execute("""
            CREATE TABLE habits (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                streak INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        print("SUCCESS! Database has been reset completely.")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reset_database()