import pymysql
import config


class Database:
    def __init__(self):
        """Open database connection when object is created."""
        self.__connection = None

        try:
            self.__connection= pymysql.connect(
                host=config.MYSQL_HOST,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                database=config.MYSQL_DATABASE,
                cursorclass=pymysql.cursors.DictCursor,
            )

            print("Database connected successfully!")

        except pymysql.MySQLError as e:
            print("Database connection failed")
            print("Error:", e)

   
    def is_connected(self):
        return self.__connection is not None

    # -----------------------------
    # Fetch One
    # -----------------------------
    def fetch_one(self, query, params=None):
        """Run query and return one result."""
        if not self.is_connected():
            print("No database connection")
            return None

        cursor = self.__connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()

        return result

    # -----------------------------__
    # Fetch All
    # -----------------------------
    def fetch_all(self, query, params=None):
        """Run query and return all results."""
        if not self.is_connected():
            print("No database connection")
            return []

        cursor = self.__connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()

        return results

   
    def execute(self, query, params=None):
        """Run INSERT, UPDATE, DELETE queries."""
        if not self.is_connected():
            print("No database connection")
            return

        cursor = self.__connection.cursor()
        cursor.execute(query, params)
        self.__connection.commit()
        cursor.close()

    # -----------------------------
    # Close Connection
    # -----------------------------
    def close(self):
        """Close database connection."""
        if self.__connection:
            self.__connection.close()
            print("Database connection closed")

    # -----------------------------
    # Create Tables
    # -----------------------------
    @staticmethod
    def create_tables():
        """Create database tables if they don't exist."""

        db = Database()

        if not db.is_connected():
            print("\nIMPORTANT:")
            print("Create the database first in MySQL:")
            print("CREATE DATABASE class_db;")
            return

        # Create users table
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        
        admin = db.fetch_one(
            "SELECT * FROM users WHERE email = %s",
            ("admin@admin.com",)
        )

        
        if not admin:
            from werkzeug.security import generate_password_hash

            db.execute(
                """
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    "Admin",
                    "admin@admin.com",
                    generate_password_hash("admin123"),
                    "admin",
                ),
            )

            print("Default admin created!")

        db.close()