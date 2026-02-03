from fastapi import FastAPI, HTTPException
import redis
import requests
import json
from config import WEATHER_API_KEY, REDIS_HOST, REDIS_PORT, CACHE_EXPIRY

app = FastAPI(title="Weather API")

# Redis client (safe initialization)
try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True,
        socket_connect_timeout=2
    )
    redis_client.ping()
except Exception:
    redis_client = None  # Redis unavailable

WEATHER_URL = (
    "https://weather.visualcrossing.com/VisualCrossingWebServices/"
    "rest/services/timeline/{city}?key={api_key}"
)

@app.get("/")
def root():
    return {"message": "Weather API is running"}

@app.get("/weather")
def get_weather(city: str):
    cache_key = f"weather:{city.lower()}"

    # Check cache (if Redis is available)
    if redis_client:
        try:
            cached_data = redis_client.get(cache_key)
            if cached_data:
                return {
                    "source": "cache",
                    "data": json.loads(cached_data)
                }
        except Exception:
            pass  # Ignore cache errors

    # Call 3rd-party API
    url = WEATHER_URL.format(city=city, api_key=WEATHER_API_KEY)

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Weather service unavailable"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail="Invalid city or weather service error"
        )

    weather_data = response.json()

    # Save to cache (best effort)
    if redis_client:
        try:
            redis_client.setex(
                cache_key,
                CACHE_EXPIRY,
                json.dumps(weather_data)
            )
        except Exception:
            pass

    return {
        "source": "api",
        "data": weather_data
    }
