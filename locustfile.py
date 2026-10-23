from locust import HttpUser, task, between
import random

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # توليد بيانات مستخدم فريدة لكل مستخدم وهمي
        self.username = f"user{random.randint(1000, 9999)}"
        self.email = f"{self.username}@example.com"
        self.password = "123456"

        # 1. تسجيل مستخدم جديد
        self.client.post("/register", data={
            "username": self.username,
            "email": self.email,
            "password": self.password
        })

        # 2. تسجيل الدخول
        self.client.post("/login", data={
            "email": self.email,
            "password": self.password
        })

    @task
    def like_and_comment(self):
        self.client.post("/home", data={
            "like_post_id": "1"
        })

        # 4. إضافة تعليق
        self.client.post("/home", data={
            "post_id": "1",
            "comment_text": "Great post!"
        })

        # 5. تسجيل الخروج
        self.client.get("/logout")
