import os
from flask import Flask, render_template, request, redirect, session, url_for
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from config import SECRET_KEY
from db import get_db

app = Flask(__name__)
app.secret_key = SECRET_KEY

# إعداد CSRF
app.config['WTF_CSRF_ENABLED'] = os.environ.get('FLASK_ENV') != 'testing'
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn, cursor = get_db()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)
        profile_picture_url = "default.jpg"

        try:
            cursor.execute(
                "INSERT INTO users (username, email, password, profile_picture_url) VALUES (%s, %s, %s, %s)",
                (username, email, hashed_pw, profile_picture_url)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            print("❌ Error:", e)
        finally:
            conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn, cursor = get_db()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['user_id']
                return redirect(url_for('home'))
        except Exception as e:
            print("❌ Login Error:", e)
        finally:
            conn.close()

    return render_template('login.html')

def get_user_by_id(user_id):
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn, cursor = get_db()

    if request.method == 'POST':
        if 'comment_text' in request.form and request.form.get('post_id'):
            post_id = request.form['post_id']
            comment_text = request.form['comment_text'].strip()
            if comment_text:
                cursor.execute(
                    "INSERT INTO comments (post_id, user_id, comment_text) VALUES (%s, %s, %s)",
                    (post_id, user_id, comment_text)
                )
                conn.commit()



        elif 'like_post_id' in request.form and request.form.get('like_post_id'):

            post_id = request.form['like_post_id']

            cursor.execute("SELECT * FROM likes WHERE post_id = %s AND user_id = %s", (post_id, user_id))

            existing_like = cursor.fetchone()

            if existing_like:

                cursor.execute("DELETE FROM likes WHERE post_id = %s AND user_id = %s", (post_id, user_id))

            else:

                cursor.execute("INSERT INTO likes (post_id, user_id) VALUES (%s, %s)", (post_id, user_id))

            conn.commit()

    cursor.execute("""
        SELECT posts.*, users.username, users.profile_picture_url 
        FROM posts 
        JOIN users ON posts.user_id = users.user_id 
        ORDER BY posts.created_at DESC
    """)
    posts = cursor.fetchall()

    cursor.execute("""
        SELECT comments.*, users.username 
        FROM comments 
        JOIN users ON comments.user_id = users.user_id
    """)
    comments = cursor.fetchall()

    cursor.execute("""
        SELECT post_id, COUNT(*) as like_count 
        FROM likes 
        GROUP BY post_id
    """)
    likes = cursor.fetchall()
    like_counts = {like['post_id']: like['like_count'] for like in likes}

    def user_has_liked(post_id):
        cursor.execute("SELECT * FROM likes WHERE post_id = %s AND user_id = %s", (post_id, user_id))
        return cursor.fetchone() is not None

    current_user = get_user_by_id(user_id)
    conn.close()

    return render_template(
        'home.html',
        posts=posts,
        comments=comments,
        like_counts=like_counts,
        user_has_liked=user_has_liked,
        current_user=current_user
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
