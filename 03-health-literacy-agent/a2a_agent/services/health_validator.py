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
            'sleep', 'vitamin', 'weight', 'workout', 'yoga', 'meditation',
            'cancer', 'diabetes', 'heart', 'lung', 'brain', 'blood'
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
    
    # LESS restrictive off-topic filters
    STRONG_OFF_TOPIC_KEYWORDS = [
        # Finance
        'bitcoin', 'crypto', 'stock', 'investment', 'money', 'bank', 'finance',
        'currency', 'trading', 'market', 'economy',
        
        # Technology (but allow health tech)
        'javascript', 'python', 'react', 'website', 'app development',
        
        # Entertainment
        'movie', 'music', 'game', 'sport', 'celebrity', 'entertainment',
        
        # Other
        'weather', 'travel', 'car repair', 'pet care'
    ]
    
    def is_health_related(self, user_message):
        """More permissive health topic detection"""
        if not user_message or len(user_message.strip()) < 2:
            logger.debug(f"Message too short: '{user_message}'")
            return False
        
        message_lower = user_message.lower()
        
        # ONLY block clearly off-topic
        if any(off_topic in message_lower for off_topic in self.STRONG_OFF_TOPIC_KEYWORDS):
            logger.debug(f"REJECTED - Clearly off-topic: '{user_message}'")
            return False
        
        # Check for health keywords
        health_found = False
        for category, keywords in self.HEALTH_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    health_found = True
                    logger.debug(f"Health keyword found: '{keyword}' in '{user_message}'")
                    break
            if health_found:
                break
        
        # Check for question patterns
        question_patterns = [
            r'what is (.+)', r'explain (.+)', r'tell me about (.+)',
            r'meaning of (.+)', r'define (.+)', r'how does (.+) work',
            r'what are (.+)', r'can you explain (.+)', r'what causes (.+)'
        ]
        
        question_found = False
        for pattern in question_patterns:
            if re.search(pattern, message_lower):
                question_found = True
                logger.debug(f"Question pattern found: '{pattern}' in '{user_message}'")
                break
        
        # Be more permissive - if it passes the strong filter, assume health-related
        result = health_found or question_found or len(message_lower.split()) <= 4
        logger.info(f"Health validation for '{user_message}': {result}")
        return result
    