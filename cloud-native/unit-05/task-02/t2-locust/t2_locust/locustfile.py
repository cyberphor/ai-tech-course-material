from locust import HttpUser
from locust import task


class Bot(HttpUser):
    @task
    def login(self):
        self.client.post(
            url="/api/token/", json={"username": "admin", "password": "asdasd"}
        )
