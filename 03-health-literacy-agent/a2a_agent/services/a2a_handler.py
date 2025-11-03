import json
import uuid
import logging

logger = logging.getLogger(__name__)

class A2ARequestHandler:
    """Handles A2A protocol request processing"""
    
    def __init__(self, health_service):
        self.health_service = health_service
    
    def process_request(self, a2a_data):
        """Process incoming A2A request"""
        try:
            if not self._is_valid_request(a2a_data):
                return self._build_error_response(
                    a2a_data.get('id'), "Invalid A2A request structure"
                )
            
            method = a2a_data.get('method')
            
            if method == "message/send":
                return self._handle_message(a2a_data)
            elif method == "execute":
                return self._handle_execute(a2a_data)
            else:
                return self._build_error_response(
                    a2a_data.get('id'), f"Unsupported method: {method}"
                )
                
        except Exception as e:
            logger.error(f"Request processing error: {e}")
            return self._build_error_response(
                a2a_data.get('id'), f"Processing error: {str(e)}"
            )
    
    def _is_valid_request(self, data):
        """Validate A2A request structure"""
        return (
            isinstance(data, dict) and
            data.get('jsonrpc') == '2.0' and
            'id' in data
        )
    
    def _handle_message(self, a2a_data):
        """Handle message/send method"""
        from ..utils.response_builder import A2AResponseBuilder
        
        message = a2a_data.get('params', {}).get('message', {})
        user_message = self._extract_user_text(message)
        
        if not user_message:
            response_text = self._get_greeting()
        else:
            # ALWAYS use the AI service for responses
            response_text = self.health_service.explain_medical_term(user_message)
        
        return A2AResponseBuilder.build_success(
            response_text, 
            a2a_data['id'],
            message.get('taskId'),
            message.get('messageId')
        )
    
    def _extract_user_text(self, message):
        """Extract text from A2A message parts"""
        for part in message.get('parts', []):
            if part.get('kind') == 'text':
                return part.get('text', '').strip()
        return ""
    
    def _get_greeting(self):
        return "Hello! I'm HealthLiteracy AI 🩺 I help explain medical terms and health concepts. What would you like to learn about?"
    
    def _handle_execute(self, a2a_data):
        """Handle execute method"""
        from ..utils.response_builder import A2AResponseBuilder
        params = a2a_data.get('params', {})
        
        response_text = "HealthLiteracy AI is ready to assist with medical education and health information!"
        return A2AResponseBuilder.build_success(
            response_text,
            a2a_data['id'],
            params.get('contextId'),
            params.get('taskId')
        )
    
    def _build_error_response(self, request_id, message):
        from ..utils.response_builder import A2AResponseBuilder
        return A2AResponseBuilder.build_error(request_id, -32603, message)
