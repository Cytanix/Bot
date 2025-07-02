import redis
import os
from dotenv import load_dotenv
load_dotenv()

r = redis.Redis(
    host=os.getenv("DATABASE_HOST"),
    port=6379,
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

r.set("foo", "bar")
value = r.get("foo")
print(value)

try:
    pong = r.ping()
    print("Connected!" if pong else "Failed to connect.")
except redis.exceptions.ConnectionError as e:
    print("Connection failed:", e)
