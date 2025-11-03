# utils/request_logger.py
import json
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FileRequestLogger:
    """Simple file-based logging instead of database"""
    
    def __init__(self, log_file="a2a_requests.log"):
        self.log_file = log_file
    
    def log_request(self, request_data, response_data, processing_time_ms):
        """Log to file instead of database"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_data.get('id', str(uuid.uuid4())),
            "method": request_data.get('method'),
            "user_message": self._extract_message(request_data),
            "processing_time_ms": processing_time_ms,
            "response_preview": response_data[:100] + "..." if len(response_data) > 100 else response_data
        }
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            logger.error(f"Failed to log request: {e}")
    
    def _extract_message(self, request_data):
        """Extract user message from A2A request"""
        message = request_data.get('params', {}).get('message', {})
        for part in message.get('parts', []):
            if part.get('kind') == 'text':
                return part.get('text', '')[:50]  # First 50 chars
        return ""
    