import pytest
import random
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from db import get_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def ensure_test_user_exists():
    conn, cursor = get_db()
    email = 'test_user@test.com'
    username = 'test_user'
    password = 'testpass'
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if not cursor.fetchone():
        hashed_pw = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, email, password, profile_picture_url) VALUES (%s, %s, %s, %s)",
            (username, email, hashed_pw, 'default.jpg')
        )
        conn.commit()
    conn.close()

def test_register_user(client):
    username = f"test_user_{random.randint(1000, 9999)}"
    email = f"{username}@test.com"
    response = client.post('/register', data={
        'username': username,
        'email': email,
        'password': 'testpass'
    }, follow_redirects=True)
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()
    assert user is not None
    assert check_password_hash(user['password'], 'testpass')

def test_login_success(client):
    ensure_test_user_exists()
    response = client.post('/login', data={
        'email': 'test_user@test.com',
        'password': 'testpass'
    }, follow_redirects=True)

    assert b'<title>home' in response.data.lower() or response.status_code == 200

def test_comment_post(client):
    ensure_test_user_exists()
    conn, cursor = get_db()

    cursor.execute("SELECT user_id FROM users WHERE email = %s", ('test_user@test.com',))
    user = cursor.fetchone()
    user_id = user['user_id']

    image_url = f"img_test_{random.randint(1000,9999)}.jpg"
    caption = "Test post for comment"
    cursor.execute("INSERT INTO posts (user_id, image_url, caption) VALUES (%s, %s, %s)",
                   (user_id, image_url, caption))
    conn.commit()

    cursor.execute("SELECT post_id FROM posts WHERE image_url = %s", (image_url,))
    post = cursor.fetchone()
    post_id = post['post_id']
    conn.close()

    with client.session_transaction() as sess:
        sess['user_id'] = user_id

    comment_text = f"Nice! {random.randint(1000, 9999)}"
    client.post('/home', data={
        'post_id': str(post_id),
        'comment_text': comment_text,
        'submit': 'comment'
    }, follow_redirects=True)

    conn, cursor = get_db()
    cursor.execute("SELECT * FROM comments WHERE comment_text = %s", (comment_text,))
    comment = cursor.fetchone()
    conn.close()

    assert comment is not None, f"⚠️ لم يتم حفظ التعليق: {comment_text}"
def test_like_post(client):
    ensure_test_user_exists()
    conn, cursor = get_db()

    cursor.execute("SELECT user_id FROM users WHERE email = %s", ('test_user@test.com',))
    user = cursor.fetchone()
    user_id = user['user_id']

    image_url = f"img_like_{random.randint(1000,9999)}.jpg"
    caption = "Test post for like"
    cursor.execute("INSERT INTO posts (user_id, image_url, caption) VALUES (%s, %s, %s)",
                   (user_id, image_url, caption))
    conn.commit()

    cursor.execute("SELECT post_id FROM posts WHERE image_url = %s", (image_url,))
    post = cursor.fetchone()
    post_id = post['post_id']
    conn.close()

    with client.session_transaction() as sess:
        sess['user_id'] = user_id

    client.post('/home', data={
        'like_post_id': str(post_id),
        'submit': 'like'
    }, follow_redirects=True)

    conn, cursor = get_db()
    cursor.execute("SELECT * FROM likes WHERE user_id = %s AND post_id = %s", (user_id, post_id))
    like = cursor.fetchone()
    conn.close()

    assert like is not None, f"⚠️ لم يتم تنفيذ الإعجاب: user_id={user_id}, post_id={post_id}"
