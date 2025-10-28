# Country Currency & Exchange API

A Django REST API for managing country data with currency exchange rates and GDP estimates. Built for HNG Backend Task.

## Features

- ✅ Fetch country data from REST Countries API
- ✅ Get exchange rates from Open Exchange Rates API  
- ✅ Calculate estimated GDP based on population and exchange rates
- ✅ CRUD operations for country data
- ✅ Filtering and sorting capabilities
- ✅ Summary image generation
- ✅ MySQL database integration
- ✅ Proper error handling and validation

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/countries/refresh/` | Fetch all countries and exchange rates, then cache in database |
| `GET` | `/api/countries/` | Get all countries (supports filtering and sorting) |
| `GET` | `/api/countries/{name}/` | Get one country by name |
| `DELETE` | `/api/countries/{name}/` | Delete a country record |
| `GET` | `/api/status/` | Show total countries and last refresh timestamp |
| `GET` | `/api/countries/image/` | Serve summary image with statistics |

## Query Parameters

### Filtering
- `region` - Filter by region (e.g., `?region=Africa`)
- `currency` - Filter by currency code (e.g., `?currency=NGN`)

### Sorting
- `sort=gdp_desc` - Sort by GDP descending
- `sort=gdp_asc` - Sort by GDP ascending  
- `sort=population_desc` - Sort by population descending
- `sort=population_asc` - Sort by population ascending
- `sort=name_asc` - Sort by name ascending (default)
- `sort=name_desc` - Sort by name descending

## Setup Instructions

### Prerequisites
- Python 3.13+
- MySQL 9.4+ or SQLite
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/jubriltayo/hng-tasks.git
cd 02-country-exchange-rates
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment configuration**
Create `.env` file:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

For MySQL:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=railway
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

5. **Database setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Run development server**
```bash
python manage.py runserver
```

API will be available at `http://localhost:8000/api/`

## Project Structure
```
02-country-exchange-rates/
├── core/                 # Django project settings
├── countries/           # Main app with API logic
│   ├── models.py       # Country and SystemStatus models
│   ├── views.py        # API viewset and endpoints
│   ├── serializers.py  # DRF serializers
│   ├── utils/          # External API clients and image generator
│   └── filters.py      # Custom filters for countries
├── cache/              # Generated summary images
├── db.sqlite3         # SQLite database (development)
├── requirements.txt   # Python dependencies
└── manage.py         # Django management script
```

## Sample Usage

### Refresh Country Data
```bash
curl -X POST http://localhost:8000/api/countries/refresh/
```

### Get African Countries
```bash
curl "http://localhost:8000/api/countries/?region=Africa"
```

### Get Countries Sorted by GDP
```bash
curl "http://localhost:8000/api/countries/?sort=gdp_desc"
```

### Get System Status
```bash
curl http://localhost:8000/api/status/
```

### Get Summary Image
```bash
curl http://localhost:8000/api/countries/image/ -o summary.png
```

## Response Examples

### Country List
```json
[
  {
    "id": 1,
    "name": "Nigeria",
    "capital": "Abuja",
    "region": "Africa",
    "population": 206139589,
    "currency_code": "NGN",
    "exchange_rate": 1600.23,
    "estimated_gdp": 25767448125.2,
    "flag_url": "https://flagcdn.com/ng.svg",
    "last_refreshed_at": "2025-10-22T18:00:00Z"
  }
]
```

### System Status
```json
{
  "total_countries": 250,
  "last_refreshed_at": "2025-10-22T18:00:00Z"
}
```

## Error Handling

The API returns consistent error responses:

- `400 Bad Request` - Validation errors
- `404 Not Found` - Resource not found
- `503 Service Unavailable` - External API errors
- `500 Internal Server Error` - Server errors

Example error response:
```json
{
  "error": "Country not found"
}
```

## External APIs Used

- **Countries Data**: https://restcountries.com/v2/all
- **Exchange Rates**: https://open.er-api.com/v6/latest/USD

## GDP Calculation

Estimated GDP is calculated using:
```
estimated_gdp = population × random(1000–2000) ÷ exchange_rate
```

## Deployment

The application can be deployed on various platforms:

### Railway
```bash
railway deploy
```

## Technologies Used

- **Backend**: Django 5.2.7, Django REST Framework
- **Database**: MySQL / SQLite
- **Image Generation**: Pillow (PIL)
- **HTTP Client**: Requests
- **Environment Management**: python-dotenv

## License

This project is part of HNG Backend Task.