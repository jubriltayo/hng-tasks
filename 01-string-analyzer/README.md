# String Analyzer Service

A RESTful API service built with Django REST Framework that analyzes strings and stores their computed properties.

## Features

- ✅ Create and analyze strings with automatic property computation
- ✅ SHA-256 hash generation for unique identification
- ✅ Palindrome detection (case-insensitive)
- ✅ Character frequency mapping
- ✅ Word counting and unique character analysis
- ✅ Advanced filtering with multiple parameters
- ✅ Natural language query parsing
- ✅ Full CRUD operations

## Tech Stack

- Python 3.13+
- Django 5.2+
- Django REST Framework 3.16+
- SQLite

## Installation & Setup

### 1. Clone and Navigate to Project

```bash
cd hng-task-1
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Project Structure

Create the following structure:

```
hng-task-1/
├── manage.py
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── api/
    ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── migrations/
```

### 5. Configure Django Settings

In `core/settings.py`, add the configurations from the provided `settings.py` artifact.

### 6. Configure Main URLs

In `core/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
]
```

### 7. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 9. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Create/Analyze String

**POST** `/strings`

```bash
curl -X POST http://localhost:8000/strings \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'
```

**Response (201 Created):**
```json
{
  "id": "abc123...",
  "value": "racecar",
  "properties": {
    "length": 7,
    "is_palindrome": true,
    "unique_characters": 4,
    "word_count": 1,
    "sha256_hash": "abc123...",
    "character_frequency_map": {
      "r": 2,
      "a": 2,
      "c": 2,
      "e": 1
    }
  },
  "created_at": "2025-10-21T10:00:00Z"
}
```

### 2. Get Specific String

**GET** `/strings/{string_value}`

```bash
curl http://localhost:8000/strings/racecar
```

### 3. Get All Strings with Filters

**GET** `/strings?is_palindrome=true&min_length=5&max_length=20&word_count=1&contains_character=a`

```bash
curl "http://localhost:8000/strings?is_palindrome=true&word_count=1"
```

**Query Parameters:**
- `is_palindrome`: boolean (true/false)
- `min_length`: integer
- `max_length`: integer
- `word_count`: integer
- `contains_character`: single character

### 4. Natural Language Filtering

**GET** `/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings`

```bash
curl "http://localhost:8000/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings"
```

**Supported Queries:**
- "all single word palindromic strings"
- "strings longer than 10 characters"
- "palindromic strings that contain the first vowel"
- "strings containing the letter z"

### 5. Delete String

**DELETE** `/strings/{string_value}`

```bash
curl -X DELETE http://localhost:8000/strings/racecar
```

## Error Responses

- **400 Bad Request**: Invalid request body or query parameters
- **404 Not Found**: String does not exist
- **409 Conflict**: String already exists
- **422 Unprocessable Entity**: Invalid data type

## Testing with Postman

1. Import the following collection:
   - Base URL: `http://localhost:8000`
   - Add requests for each endpoint listed above

2. Test the complete flow:
   - Create a palindrome: `{"value": "racecar"}`
   - Create a non-palindrome: `{"value": "hello world"}`
   - Filter by palindrome: `/strings?is_palindrome=true`
   - Use natural language: `/strings/filter-by-natural-language?query=single word palindromic strings`
   - Delete a string

## Production Deployment

### Using PostgreSQL

1. Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

2. Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'string_analyzer_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. Set DEBUG to False and configure ALLOWED_HOSTS

### Using Gunicorn

```bash
pip install gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

## Performance Considerations

- Database indexes are created on `is_palindrome`, `word_count`, and `length` fields
- SHA-256 hashing ensures unique identification
- Character frequency maps are stored as JSON for efficient querying

## API Design Decisions

1. **SHA-256 as Primary Key**: Ensures uniqueness and provides cryptographic hash benefits
2. **Case-Insensitive Palindrome**: More intuitive for most use cases
3. **Natural Language Parsing**: Uses regex patterns for common query structures
4. **Character Frequency in JSON**: Allows flexible querying without additional tables

## Troubleshooting

### Issue: "String already exists" error
**Solution**: The string value must be unique. Delete the existing string first or use a different value.

### Issue: Natural language query returns no results
**Solution**: Check the interpreted filters in the response to see how your query was parsed. Adjust your query to match supported patterns.

### Issue: 404 on string retrieval
**Solution**: Ensure you're using the exact string value (case-sensitive) in the URL path.
