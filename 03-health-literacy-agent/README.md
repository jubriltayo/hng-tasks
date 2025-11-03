# Health Literacy AI Agent

A professional AI-powered health education assistant that provides clear, accessible explanations of medical terms and health concepts. Built with Django and integrated with Telex.im via the A2A protocol.

## 🚀 Features

- **AI-Powered Health Education**: Uses Google's Gemini AI to explain medical terms in simple, understandable language
- **Telex.im Integration**: Seamlessly connects with Telex platform using A2A JSON-RPC protocol
- **Health Topic Validation**: Intelligent filtering to ensure responses stay within health and wellness topics
- **Production Ready**: Secure, scalable Django backend deployed on Railway
- **Professional Medical Boundaries**: Never provides diagnoses - focuses on educational content only

## 🏗️ Architecture

```
Health Literacy Agent
├── Django Backend (Python)
│   ├── A2A Protocol Handler
│   ├── Gemini AI Service
│   ├── Health Topic Validator
│   └── Response Builder
└── Telex.im Integration
    ├── A2A JSON-RPC Endpoints
    ├── Workflow Configuration
    └── Skill Registration
```

## 🛠️ Technology Stack

- **Backend**: Django 5.2.7, Python 3.10
- **AI Model**: Google Gemini 2.5 Flash
- **Protocol**: A2A JSON-RPC 2.0
- **Deployment**: Railway
- **Integration**: Telex.im A2A Protocol

## 📋 Prerequisites

- Python 3.10+
- Google Gemini API Key
- Telex.im Account (for integration)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/jubriltayo/hng-tasks.git
cd 03-health-literacy-agent
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file:
```bash
SECRET_KEY=your-django-secret-key
DEBUG=True
GEMINI_API_KEY=your-gemini-api-key
```

Generate a secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Database Setup
```bash
python manage.py migrate
```

### 6. Run Development Server
```bash
python manage.py runserver
```

## 🌐 API Endpoints

### Health Check
```http
GET /api/health
```
Returns service status and Gemini AI availability.

### A2A Agent Endpoint
```http
POST /api/a2a/health
```
Main A2A protocol endpoint for Telex integration.

## 🔌 Telex Integration

### Workflow JSON
```json
{
  "active": true,
  "category": "health",
  "description": "AI health education assistant that explains medical terms",
  "nodes": [
    {
      "id": "health_agent",
      "name": "Health Literacy Agent",
      "type": "a2a/mastra-a2a-node",
      "url": "https://hng-tasks-production-de98.up.railway.app/api/a2a/health"
    }
  ]
}
```

### Required Skills
- A2A Protocol Skills (Chess A2A, Weather A2A, Capitalizer A2A)
- Health/Education category skills

## 🚀 Deployment

### Railway Deployment
1. Connect your repository to Railway
2. Set environment variables:
   - `SECRET_KEY`
   - `GEMINI_API_KEY` 
   - `DEBUG=False`
3. Deploy automatically on git push

### Environment Variables
```bash
SECRET_KEY=your-production-secret-key
GEMINI_API_KEY=your-gemini-api-key
DEBUG=False
DOMAIN=your-production-domain.com  # Optional
```

## 🧪 Testing

### Local Testing
```bash
# Health check
curl http://localhost:8000/api/health

# A2A endpoint test
curl -X POST http://localhost:8000/api/a2a/health \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-001",
    "method": "message/send",
    "params": {
      "message": {
        "kind": "message",
        "role": "user",
        "parts": [{"kind": "text", "text": "What is diabetes?"}]
      }
    }
  }'
```

### Production Testing
Replace `localhost:8000` with your production domain.

## 📁 Project Structure

```
health-literacy-agent/
├── a2a_agent/
│   ├── services/
│   │   ├── a2a_handler.py
│   │   ├── gemini_service.py
│   │   └── health_validator.py
│   ├── views/
│   │   ├── a2a_views.py
│   │   └── health_views.py
│   ├── utils/
│   │   ├── response_builder.py
│   │   └── error_handler.py
│   └── urls.py
├── core/
│   ├── settings.py
│   └── urls.py
├── requirements.txt
├── Procfile
└── runtime.txt
```

## 🔒 Security Features

- Production-grade Django security settings
- CORS configuration for Telex domains
- Environment variable protection
- Health topic validation to prevent off-topic responses
- No medical diagnoses or treatment advice

## 📈 Monitoring

### Health Endpoint
```bash
curl https://your-domain.com/api/health
```

### Telex Agent Logs
```
https://api.telex.im/agent-logs/{channel-id}.txt
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check Telex integration documentation
2. Review Django logs for errors
3. Verify Gemini API key configuration
4. Test A2A protocol compliance

## 🎯 Use Cases

- **Patient Education**: Explain medical conditions and treatments
- **Health Literacy**: Simplify complex medical terminology
- **Wellness Coaching**: Provide general health information
- **Medical Training**: Educational tool for healthcare students

## ⚠️ Important Notes

- This agent provides educational information only
- Never replaces professional medical advice
- Always consult healthcare professionals for medical concerns
- Responses are generated by AI and should be verified
