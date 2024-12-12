class ResponseBody:
    def __init__(self, message_request, bot_response, need_correction, status_code, error_message=""):
        self.message_request = message_request
        self.bot_response = bot_response
        self.need_correction = need_correction
        self.status_code = status_code
        self.error_message = error_message
        
    def to_dict(self):
        return {
            "message_request": self.message_request,
            "bot_response": self.bot_response,
            "need_correction": self.need_correction,
            "status_code": self.status_code,
            "error_message": self.error_message,
        }