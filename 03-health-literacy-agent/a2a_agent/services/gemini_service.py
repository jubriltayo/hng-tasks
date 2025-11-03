import os
import logging
from .health_validator import HealthTopicValidator

logger = logging.getLogger(__name__)

class GeminiHealthService:
    """
    Proper AI agent that uses Gemini 2.5 Flash as its brain
    """
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.available = False
        self.validator = HealthTopicValidator()
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Gemini AI client with 2.5 Flash"""
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found - running in fallback mode")
            return
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.available = True
            logger.info("Gemini 2.5 Flash Health Service initialized successfully")
        except Exception as e:
            logger.error(f"Gemini initialization failed: {e}")
    
    def explain_medical_term(self, user_message):
        """
        Use AI model to generate responses for ANY health topic
        """
        logger.info(f"AI Agent processing: '{user_message}'")
        
        # First, validate it's health-related
        if not self.validator.is_health_related(user_message):
            return self._get_off_topic_rejection()
        
        # If Gemini is available, USE IT as the primary brain
        if self.available:
            try:
                response = self._get_ai_response(user_message)
                if response:
                    return response
            except Exception as e:
                logger.error(f"Gemini API error, using fallback: {e}")
        
        # Only use fallback if AI completely fails
        return self._get_simple_fallback(user_message)
    
    def _get_ai_response(self, user_message):
        """Get response from Gemini AI"""
        try:
            prompt = self._build_health_prompt(user_message)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            return None
    
    def _build_health_prompt(self, user_message):
        """Build intelligent health education prompt"""
        return f"""
        You are HealthLiteracy AI - a friendly health education assistant.
        
        GUIDELINES:
        - Explain medical/health concepts in simple, easy-to-understand language
        - Keep responses educational and under 150 words
        - Focus on general knowledge, prevention, and healthy practices
        - NEVER provide medical diagnoses or treatment plans
        - Always remind users to consult healthcare professionals for personal advice
        - Be encouraging and supportive
        
        USER QUESTION: "{user_message}"
        
        Provide a helpful, educational response about this health topic:
        """
    
    def _get_off_topic_rejection(self):
        """Standard off-topic rejection"""
        return "I specialize only in health and wellness topics. I can help with nutrition, exercise, mental health, sleep, or other health-related questions!"
    
    def _get_simple_fallback(self, user_message):
        """Simple fallback when AI fails"""
        return f"I'd love to help explain '{user_message}'! However, I'm experiencing technical difficulties with my knowledge base. Please consult reliable health resources or healthcare professionals for accurate information about this topic."
    
    def is_health_related(self, user_message):
        """Delegate to validator"""
        return self.validator.is_health_related(user_message)