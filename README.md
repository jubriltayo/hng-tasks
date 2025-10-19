
# 🐍 Django API — Me Endpoint

A simple Django REST API that returns user information along with a random cat fact fetched from [Cat Fact API](https://catfact.ninja/).  
This project is perfect for quick deployment and testing basic Django REST Framework concepts.

---

## 📂 Project Structure

```
hng-task-0/
├── core/
│   ├── **init**.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── me/
│   ├── **init**.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── manage.py
└── requirements.txt

````

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/jubriltayo/hng-task-0.git
cd hng-task-0
````

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Then update `settings.py` accordingly.


### 4. Start the Development Server

```bash
python manage.py runserver
```

Visit: [http://localhost:8000/me/](http://localhost:8000/me/)

---

## 🧪 API Endpoint

### `GET /me/`

**Response 200 OK**

```json
{
    "status": "success",
    "user": {
        "email": "jubriltayo@gmail.com",
        "name": "Tayo Jubril",
        "stack": "Python (Django, FastAPI, Flask), JavaScript (Node.js, React, Next.js), PHP (Laravel)"
    },
    "timestamp": "2025-10-19T14:00:04.109183+00:00",
    "fact": "Cats have supersonic hearing"
}
```

---

## 🧰 Dependencies

* Python 3.10+
* Django
* Django REST Framework
* Requests

Install with:

```bash
pip install -r requirements.txt
```

---

## 🧑 Author

**Tayo Jubril**
📧 [jubriltayo@gmail.com](mailto:jubriltayo@gmail.com)

GitHub Repo: [https://github.com/jubriltayo/hng-task-0](https://github.com/jubriltayo/hng-task-0)
