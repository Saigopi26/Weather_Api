# 🌦️ Weather API (FastAPI + Redis + 3rd-Party API)

A simple **Weather API** built using **FastAPI** that fetches weather data from a **3rd-party weather service (Visual Crossing)** and uses **Redis** for caching to improve performance and reduce external API calls.

This project demonstrates:

* Working with **3rd-party APIs**
* **Redis caching** with TTL
* **Environment variables** for secrets
* Graceful error handling
* Production-ready API patterns

---

## 🚀 Features

* Fetch real-time weather by city
* Cache weather data in Redis
* Automatic cache expiry (TTL)
* Works even if Redis is unavailable
* FastAPI auto-generated Swagger docs

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **FastAPI** – Web framework
* **Uvicorn** – ASGI server
* **Redis** – In-memory cache
* **Requests** – HTTP client
* **Visual Crossing Weather API** – Weather data provider

---

## 📁 Project Structure

```text
Weather_Api/
│── main.py            # FastAPI application
│── config.py          # Environment configuration
│── requirements.txt   # Dependencies
│── .env               # Environment variables (not committed)
│── README.md          # Project documentation
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
WEATHER_API_KEY=your_visual_crossing_api_key
REDIS_HOST=localhost
REDIS_PORT=6379
CACHE_EXPIRY=43200
```

> `CACHE_EXPIRY` is in seconds (43200 = 12 hours)

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧠 Redis Setup

### Option 1: Using Docker (Recommended)

```bash
docker run -d -p 6379:6379 --name redis redis
```

### Option 2: Without Redis

The API will still work. Redis is used as **best-effort caching** and failures are handled gracefully.

---

## ▶️ Run the Application

```bash
uvicorn main:app --reload
```

Server will start at:

```text
http://127.0.0.1:8000
```

---

## 📘 API Documentation (Swagger)

FastAPI provides interactive API docs automatically:

* Swagger UI:

  ```
  http://127.0.0.1:8000/docs
  ```

* ReDoc:

  ```
  http://127.0.0.1:8000/redoc
  ```

---

## 🌍 API Endpoints

### 1️⃣ Health Check

```http
GET /
```

Response:

```json
{
  "message": "Weather API is running"
}
```

---

### 2️⃣ Get Weather by City

```http
GET /weather?city=Newyork
```

#### Query Params

| Name | Type   | Required | Description |
| ---- | ------ | -------- | ----------- |
| city | string | ✅        | City name   |

#### Sample Response

```json
{
  "source": "api",
  "data": {
    "address": "New York",
    "days": [
      {
        "temp": 6.2,
        "humidity": 71
      }
    ]
  }
}
```

* `source = api` → fetched from 3rd-party API
* `source = cache` → served from Redis

---

## ⏱️ Caching Strategy

* Cache key: `weather:<city>`
* TTL controlled by `CACHE_EXPIRY`
* Reduces API calls & improves response time

---

## ❌ Error Handling

| Status Code | Reason                      |
| ----------- | --------------------------- |
| 400         | Invalid city name           |
| 503         | Weather service unavailable |
| 200         | Success                     |

Redis failures **do not break the API**.

---

## 🧪 Testing Examples

### Browser

```
http://127.0.0.1:8000/weather?city=London
```

### cURL

```bash
curl "http://127.0.0.1:8000/weather?city=London"
```

---

## 🎯 Interview-Ready Summary

> This project is a FastAPI-based Weather API that integrates with a third-party weather service and uses Redis for caching. It follows best practices such as environment-based configuration, graceful degradation when Redis is unavailable, proper timeout handling, and API documentation using Swagger.

---

## 🔮 Future Enhancements

* Add `/forecast` endpoint
* City + country support
* Rate limiting
* Docker Compose (FastAPI + Redis)
* Unit tests with mocked APIs

---

## 👨‍💻 Author
### SaiGopi
Built as a learning and interview-ready project for working with **3rd-party APIs and caching**.

# Project URL
[Weather_API](https://roadmap.sh/projects/weather-api-wrapper-service)
