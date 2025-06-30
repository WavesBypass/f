from locust import HttpUser, task, between
import random
import string

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X)",
    "Mozilla/5.0 (Android 11; Mobile)",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)",
]

ENDPOINTS = [
    "/", "/login", "/about", "/contact", "/api/data", "/search", "/random",
    "/update", "/delete", "/heavy_process"
]

HTTP_METHODS = ["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE"]


def random_query_string():
    length = random.randint(10, 25)
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=length))


def random_post_payload():
    return {
        "username":
        ''.join(random.choices(string.ascii_letters, k=20)),
        "password":
        ''.join(random.choices(string.ascii_letters + string.digits, k=30)),
        "data":
        ''.join(random.choices(string.printable * 10, k=1000))  # Large payload
    }


class AggressiveUser(HttpUser):
    wait_time = between(0.01, 0.03)  # Ultra aggressive timing

    @task(10)
    def load_requests(self):
        method = random.choice(HTTP_METHODS)
        endpoint = random.choice(ENDPOINTS)
        url = endpoint

        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }

        if "?" not in url and random.random() < 0.9:
            url += "?q=" + random_query_string()

        if method == "GET":
            self.client.get(url, headers=headers, timeout=15)
        elif method == "POST":
            payload = random_post_payload()
            self.client.post(url, json=payload, headers=headers, timeout=15)
        elif method == "HEAD":
            self.client.head(url, headers=headers, timeout=15)
        elif method == "OPTIONS":
            self.client.options(url, headers=headers, timeout=15)
        elif method == "PUT":
            payload = random_post_payload()
            self.client.put(url, json=payload, headers=headers, timeout=15)
        elif method == "DELETE":
            self.client.delete(url, headers=headers, timeout=15)
