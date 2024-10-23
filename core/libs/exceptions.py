class MinorError(Exception):
    default_status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__(message) 
        self.message = message
        self.status_code = status_code or self.default_status_code 

    def to_dict(self):
        return {
            'message': self.message,
            'status_code': self.status_code
        }
    
