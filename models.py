import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    """Database connection and cursor management."""
    def __init__(self):
        self.connection = MySQLdb.connect(
            host='localhost',
            user='root',
            password='',
            database='Inkom'
        )
        self.cursor = self.connection.cursor()

    def close(self):
        """Close the database connection and cursor."""
        self.cursor.close()
        self.connection.close()


class User:
    """User model for managing user-related operations."""
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def create_user(username, password):
        """Create a new user."""
        db = Database()
        password_hash = generate_password_hash(password)
        db.cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash)
        )
        db.connection.commit()
        db.close()

    @staticmethod
    def get_user_by_username(username):
        """Retrieve a user by their username."""
        db = Database()
        db.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = db.cursor.fetchone()
        db.close()
        return user

    @staticmethod
    def verify_password(username, password):
        """Verify a user's password."""
        db = Database()
        db.cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = db.cursor.fetchone()
        db.close()
        return check_password_hash(result[0], password) if result else False

    @staticmethod
    def update_password(username, new_password):
        """Update a user's password."""
        db = Database()
        password_hash = generate_password_hash(new_password)
        db.cursor.execute(
            "UPDATE users SET password_hash = %s WHERE username = %s",
            (password_hash, username)
        )
        db.connection.commit()
        db.close()



class Inventory:
    """Inventory model for managing inventory-related operations."""
    def __init__(self, namaBarang, kodeBarang, jumlahBarang, kondisiBarang, gambarBarang):
        self.namaBarang = namaBarang
        self.kodeBarang = kodeBarang
        self.jumlahBarang = jumlahBarang
        self.kondisiBarang = kondisiBarang
        self.gambarBarang = gambarBarang

    @staticmethod
    def add_item(namaBarang, kodeBarang, jumlahBarang, kondisiBarang, gambarBarang):
        """Add a new inventory item."""
        db = Database()
        db.cursor.execute(
            "INSERT INTO inventory (namaBarang, kodeBarang, jumlahBarang, kondisiBarang, gambarBarang) VALUES (%s, %s, %s, %s, %s)",
            (namaBarang, kodeBarang, jumlahBarang, kondisiBarang, gambarBarang)
        )
        db.connection.commit()
        db.close()

    @staticmethod
    def get_all_items():
        """Retrieve all inventory items."""
        db = Database()
        db.cursor.execute("SELECT * FROM inventory")
        items = db.cursor.fetchall()
        db.close()
        return items

    @staticmethod
    def get_item_by_id(item_id):
        """Retrieve a single inventory item by its ID."""
        db = Database()
        db.cursor.execute("SELECT * FROM inventory WHERE id = %s", (item_id,))
        item = db.cursor.fetchone()
        db.close()
        return item

    @staticmethod
    def update_item(item_id, namaBarang, kodeBarang, jumlahBarang, kondisiBarang, gambarBarang):
        """Update an existing inventory item."""
        db = Database()
        db.cursor.execute(
            "UPDATE inventory SET namaBarang = %s, kodeBarang = %s, jumlahBarang = %s, kondisiBarang = %s, gambarBarang = %s WHERE id = %s",
            (namaBarang, kodeBarang, jumlahBarang, kondisiBarang, gambarBarang, item_id)
        )
        db.connection.commit()
        db.close()

    @staticmethod
    def delete_item(item_id):
        """Delete an inventory item by its ID."""
        db = Database()
        db.cursor.execute("DELETE FROM inventory WHERE id = %s", (item_id,))
        db.connection.commit()
        db.close()

    @staticmethod
    def search_items(query):
        """Search for inventory items by name or code."""
        db = Database()
        db.cursor.execute(
            "SELECT * FROM inventory WHERE namaBarang LIKE %s OR kodeBarang LIKE %s",
            (f"%{query}%", f"%{query}%")
        )
        items = db.cursor.fetchall()
        db.close()
        return items

    @staticmethod
    def count_items():
        """Count the total number of inventory items."""
        db = Database()
        db.cursor.execute("SELECT COUNT(*) FROM inventory")
        count = db.cursor.fetchone()[0]
        db.close()
        return count
