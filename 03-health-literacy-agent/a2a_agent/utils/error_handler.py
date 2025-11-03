class A2AErrorHandler:
    """Standardized A2A error handling"""
    
    ERROR_CODES = {
        'PARSE_ERROR': -32700,
        'INVALID_REQUEST': -32600,
        'METHOD_NOT_FOUND': -32601,
        'INVALID_PARAMS': -32602,
        'INTERNAL_ERROR': -32603
    }
    
    @classmethod
    def invalid_request(cls, request_id, details=None):
        from .response_builder import A2AResponseBuilder
        return A2AResponseBuilder.build_error(
            request_id, cls.ERROR_CODES['INVALID_REQUEST'],
            f"Invalid Request: {details}"
        )
    
    @classmethod
    def method_not_found(cls, request_id, method_name):
        from .response_builder import A2AResponseBuilder
        return A2AResponseBuilder.build_error(
            request_id, cls.ERROR_CODES['METHOD_NOT_FOUND'],
            f"Method not found: {method_name}"
        )
    
    @classmethod
    def internal_error(cls, request_id, details=None):
        from .response_builder import A2AResponseBuilder
        return A2AResponseBuilder.build_error(
            request_id, cls.ERROR_CODES['INTERNAL_ERROR'],
            f"Internal error: {details}"
        )