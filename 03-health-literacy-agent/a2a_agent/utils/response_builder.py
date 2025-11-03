import uuid
from datetime import datetime

class A2AResponseBuilder:
    """Builds properly formatted A2A JSON-RPC responses"""
    
    @staticmethod
    def build_success(response_text, request_id, context_id=None, task_id=None):
        context_id = context_id or str(uuid.uuid4())
        task_id = task_id or str(uuid.uuid4())
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "id": task_id,
                "contextId": context_id,
                "status": {
                    "state": "completed",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "message": {
                        "messageId": str(uuid.uuid4()),
                        "role": "agent",
                        "parts": [{"kind": "text", "text": response_text}],
                        "kind": "message",
                        "taskId": task_id
                    }
                },
                "artifacts": [
                    {
                        "artifactId": str(uuid.uuid4()),
                        "name": "health_explanation",
                        "parts": [{"kind": "text", "text": response_text}]
                    }
                ],
                "history": [
                    {
                        "messageId": str(uuid.uuid4()),
                        "role": "agent", 
                        "parts": [{"kind": "text", "text": response_text}],
                        "kind": "message",
                        "taskId": task_id
                    }
                ],
                "kind": "task"
            }
        }
    
    @staticmethod
    def build_error(request_id, code, message):
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }