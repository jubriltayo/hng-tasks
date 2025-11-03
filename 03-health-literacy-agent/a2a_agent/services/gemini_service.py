import os
import logging
from .health_validator import HealthTopicValidator

logger = logging.getLogger(__name__)

class GeminiHealthService:
    """
    Pure API-based health service with STRONG topic enforcement
    """
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.available = False
        self.validator = HealthTopicValidator()
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Gemini AI client"""
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found - running in fallback mode")
            return
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')  # Your updated model
            self.available = True
            logger.info("Gemini Health Service initialized successfully")
        except Exception as e:
            logger.error(f"Gemini initialization failed: {e}")
    
    def explain_medical_term(self, user_message):
        """
        Stateless medical explanation with STRONG health focus
        """
        # LOG for debugging
        logger.info(f"Processing message: '{user_message}'")
        
        if not self.available:
            return self._get_fallback_response(user_message)
        
        try:
            # Use STRICTER prompt
            prompt = self._build_strict_health_prompt(user_message)
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # POST-PROCESSING: Double-check response doesn't contain off-topic content
            if self._contains_off_topic_response(response_text):
                logger.warning(f"Gemini generated off-topic response, using fallback: {response_text[:100]}...")
                return self._get_off_topic_rejection()
                
            return response_text
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return self._get_fallback_response(user_message)
    
    def _build_strict_health_prompt(self, user_message):
        """Build STRICT health-only prompt"""
        return f"""
        CRITICAL: You are HealthLiteracy AI - a STRICTLY health and medical education assistant.
        
        RULES:
        1. ONLY answer questions about health, medicine, wellness, nutrition, exercise, mental health, sleep, medical conditions, body systems, symptoms, treatments.
        2. If the question is NOT health-related (finance, technology, entertainment, sports, pets, etc.), respond EXACTLY:
           "I specialize only in health and wellness topics. I can help with nutrition, exercise, mental health, sleep, or other health-related questions!"
        3. Do not provide medical diagnoses; always advise consulting professionals.
        4. Keep explanations simple, educational, and under 200 words.
        
        USER QUESTION: "{user_message}"
        
        If health-related: Provide clear, educational explanation.
        If NOT health-related: Use the exact rejection message from Rule 2.
        """
    
    def _contains_off_topic_response(self, response_text):
        """Check if Gemini accidentally answered off-topic"""
        off_topic_indicators = [
            'bitcoin', 'crypto', 'stock', 'investment', 'money', 'finance',
            'movie', 'music', 'sport', 'game', 'weather', 'travel'
        ]
        response_lower = response_text.lower()
        return any(indicator in response_lower for indicator in off_topic_indicators)
    
    def _get_off_topic_rejection(self):
        """Standard off-topic rejection message"""
        return "I specialize only in health and wellness topics. I can help with nutrition, exercise, mental health, sleep, or other health-related questions!"
    
    def _get_fallback_response(self, user_message):
        """Static fallback with health focus"""
        # Only provide fallback for health topics
        if not self.is_health_related(user_message):
            return self._get_off_topic_rejection()
            
        fallback_responses = {
            "hypertension": "Hypertension (high blood pressure) occurs when blood flows with too much force through arteries. Regular monitoring is important.",
            "diabetes": "Diabetes affects how your body processes blood sugar. Proper management is key for health.",
            "asthma": "Asthma involves sensitive airways that can narrow in response to triggers.",
            "cholesterol": "Cholesterol is needed for healthy cells, but too much can increase heart disease risk."
        }
        
        user_lower = user_message.lower()
        for term, response in fallback_responses.items():
            if term in user_lower:
                return response + "\n\n💡 For personalized medical advice, consult healthcare professionals."
        
        return "I'm currently enhancing my medical knowledge. For health information, consult healthcare professionals."
    
    def is_health_related(self, user_message):
        """Validate if message is health-related with logging"""
        result = self.validator.is_health_related(user_message)
        logger.info(f"Health validation for '{user_message}': {result}")
        return result
    