import random
from db import get_db

rand_id = random.randint(1000, 9999)
username = f"test_user_{rand_id}"
email = f"{username}@example.com"

def test_connection():
    try:
        conn, cursor = get_db()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        print("✅ Database connection successful:", result)
    except Exception as e:
        print("❌ Database connection failed:", e)

def test_create_user():
    conn, cursor = get_db()
    try:
        cursor.execute("""
            INSERT INTO users (username, email, password, profile_picture_url)
            VALUES (%s, %s, %s, %s)
        """, (username, email, "hashedpass", "default.jpg"))
        conn.commit()
        print(f"✅ User '{username}' created successfully.")
    except Exception as e:
        conn.rollback()
        print("❌ Create failed:", e)
    finally:
        conn.close()

def test_read_user():
    conn, cursor = get_db()
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            print("✅ User read successfully:", user)
        else:
            print("❌ User not found.")
    except Exception as e:
        print("❌ Read failed:", e)
    finally:
        conn.close()

def test_update_user():
    conn, cursor = get_db()
    try:
        new_username = username + "_updated"
        cursor.execute("UPDATE users SET username = %s WHERE email = %s", (new_username, email))
        conn.commit()
        print("✅ User updated successfully.")
    except Exception as e:
        conn.rollback()
        print("❌ Update failed:", e)
    finally:
        conn.close()

def test_delete_user():
    conn, cursor = get_db()
    try:
        cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        conn.commit()
        print("✅ User deleted successfully.")
    except Exception as e:
        conn.rollback()
        print("❌ Delete failed:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    print(f"\n🧪 Testing with user: {username} | email: {email}\n")
    test_connection()
    test_create_user()
    test_read_user()
    test_update_user()
    test_read_user()
    test_delete_user()
    test_read_user()
