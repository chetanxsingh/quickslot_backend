# 🚀 QuickSlot Backend

A concurrency-safe sports venue booking API built with Django & Django REST Framework.  
Designed for real-time slot booking with zero double-booking guarantee.

---

## 📌 Features

- 🏟️ Venue listing with available slots
- 📅 Date-based slot viewing
- ⚡ Real-time booking with concurrency safety
- ❌ Prevents double booking (race condition safe)
- 👤 User-based booking management
- 🔁 Cancel bookings
- 🌐 REST API with clean architecture
- 🚀 Deployed on Render

---

## 🧠 Tech Stack

| Layer        | Technology |
|-------------|------------|
| Backend     | Django 5 + Django REST Framework |
| Database    | PostgreSQL (Render) / SQLite (local) |
| Server      | Gunicorn |
| Deployment  | Render |
| API Docs    | drf-spectacular |
| CORS        | django-cors-headers |
| Static Files| WhiteNoise |

---

## ⚙️ Project Structure

quickslot_backend/ │ ├── config/                # Django project config │   ├── settings.py │   ├── urls.py │ ├── apps/ │   ├── users/             # Custom user model │   ├── venues/            # Venue & slot management │   ├── bookings/          # Booking logic (core) │ ├── manage.py ├── requirements.txt ├── build.sh               # Render build script

---

## 🔥 Core Concept: Concurrency Safety

The system ensures no slot is ever double-booked, even under simultaneous requests.

### Approach:
- transaction.atomic()
- select_for_update() (DB row locking)
- DB-level constraint (OneToOne relationship)

👉 Guarantees:
> If 2 users book at the same time → only 1 succeeds.

---

## 📡 API Endpoints

### 🏟️ Venues

GET /api/venues/

---

### 📅 Slots

GET /api/venues/{id}/slots/?date=YYYY-MM-DD

---

### 🎟️ Book Slot

POST /api/bookings/

Body:
json {   "slot_id": 1 } 

---

### 👤 User Bookings

GET /api/users/{id}/bookings/

---

### ❌ Cancel Booking

DELETE /api/bookings/{id}/

---

## 🔐 Authentication

For simplicity (hackathon scope):

- Uses X-User-Id header
- No full auth system implemented

---

## 🛠️ Local Setup

### 1. Clone repo
bash git clone <repo-url> cd quickslot_backend 

---

### 2. Create virtual environment
bash python3 -m venv venv source venv/bin/activate 

---

### 3. Install dependencies
bash pip install -r requirements.txt 

---

### 4. Run migrations
bash python manage.py migrate 

---

### 5. Run server
bash python manage.py runserver 

---

## 🌍 Deployment (Render)

### Steps:

1. Push code to GitHub  
2. Create Web Service on Render  
3. Set:

Build Command
bash ./build.sh 

Start Command
bash gunicorn config.wsgi:application 

---

### Environment Variables

DJANGO_SECRET_KEY=your-secret DJANGO_DEBUG=False DJANGO_ALLOWED_HOSTS=.onrender.com DATABASE_URL=<postgres-url>

---

## 🧪 Testing Concurrency

To test double-booking prevention:

1. Open app on 2 devices  
2. Try booking same slot simultaneously  

👉 Expected:
- One success ✅  
- One failure (409 Conflict) ❌  

---

## 📈 Future Improvements

- 🔄 WebSocket-based real-time updates
- 📱 Full authentication system (JWT)
- ⚡ Redis caching
- 📊 Booking analytics dashboard
- 🧪 Unit & integration tests

---

## 🤖 AI Usage Note

AI tools were used for:
- Boilerplate generation
- API structuring
- Debugging deployment issues

Manual improvements:
- Concurrency-safe booking logic
- API validation and error handling

---

## 🏆 Hackathon Note

This project prioritizes:
- Correctness over features
- Clean architecture
- Real-world production patterns

---

## 👨‍💻 Author

Chetan Singh Rajput
