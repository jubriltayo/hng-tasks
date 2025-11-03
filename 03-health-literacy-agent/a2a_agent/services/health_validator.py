import re
import logging

logger = logging.getLogger(__name__)

class HealthTopicValidator:
    """Validates if a message is health-related and appropriate"""
    
    HEALTH_KEYWORDS = {
        'general': [
            'health', 'medical', 'medicine', 'doctor', 'hospital', 'clinic',
            'symptom', 'treatment', 'diagnosis', 'condition', 'disease',
            'pain', 'illness', 'injury', 'recovery', 'therapy', 'wellness',
            'nutrition', 'diet', 'exercise', 'fitness', 'mental', 'stress',
            'sleep', 'vitamin', 'weight', 'workout', 'yoga', 'meditation'
        ],
        'body_systems': [
            'heart', 'lung', 'brain', 'nerve', 'muscle', 'bone', 'blood',
            'digestive', 'respiratory', 'nervous', 'immune', 'cardiac',
            'liver', 'kidney', 'stomach', 'skin', 'eye', 'ear', 'thyroid'
        ],
        'common_conditions': [
            'headache', 'fever', 'cold', 'flu', 'allergy', 'infection',
            'pressure', 'sugar', 'cholesterol', 'vitamin', 'nutrition',
            'hypertension', 'diabetes', 'asthma', 'arthritis', 'cancer',
            'migraine', 'asthma', 'anemia', 'obesity', 'osteoporosis'
        ]
    }
    
    # ADD STRONG OFF-TOPIC FILTERS
    OFF_TOPIC_KEYWORDS = [
        # Finance
        'bitcoin', 'crypto', 'stock', 'investment', 'money', 'bank', 'finance',
        'currency', 'trading', 'market', 'economy', 'price', 'profit',
        
        # Technology  
        'computer', 'phone', 'software', 'programming', 'code', 'javascript',
        'python', 'react', 'website', 'app', 'digital', 'online',
        
        # Entertainment
        'movie', 'music', 'game', 'sport', 'celebrity', 'entertainment',
        'netflix', 'youtube', 'instagram', 'social media',
        
        # Other
        'weather', 'travel', 'car', 'pet', 'animal', 'dog', 'cat', 'cooking',
        'recipe', 'food recipe', 'restaurant', 'shopping', 'fashion'
    ]
    
    def is_health_related(self, user_message):
        """Check if message is health-related with debugging"""
        if not user_message or len(user_message.strip()) < 2:
            logger.debug(f"Message too short: '{user_message}'")
            return False
        
        message_lower = user_message.lower()
        
        # FIRST: Check for off-topic keywords (STRONG FILTER)
        if any(off_topic in message_lower for off_topic in self.OFF_TOPIC_KEYWORDS):
            logger.debug(f"REJECTED - Off-topic keyword detected: '{user_message}'")
            return False
        
        # SECOND: Check for health keywords
        health_found = False
        for category, keywords in self.HEALTH_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    health_found = True
                    logger.debug(f"Health keyword found: '{keyword}' in '{user_message}'")
                    break
            if health_found:
                break
        
        # THIRD: Check for medical question patterns
        question_patterns = [
            r'what is (.+)', r'explain (.+)', r'tell me about (.+)',
            r'meaning of (.+)', r'define (.+)', r'how does (.+) work',
            r'what are (.+)', r'can you explain (.+)'
        ]
        
        question_found = False
        for pattern in question_patterns:
            if re.search(pattern, message_lower):
                question_found = True
                logger.debug(f"Medical question pattern found: '{pattern}' in '{user_message}'")
                break
        
        result = health_found or question_found
        logger.debug(f"Final health_related result for '{user_message}': {result}")
        return result