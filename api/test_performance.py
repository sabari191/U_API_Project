from locust import HttpUser, task, between

class WeatherAPIUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_weather(self):
        self.client.get("/weather/London")