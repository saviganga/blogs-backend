class UserResponses:
    
    def user_error_response(self, data=None, message=None):
        if data == None and message == None:
            return {
                "status": "FAILED",
                "message": "Oops! Error",
            }
        else:
            if data:
                return {
                    "status": "FAILED",
                    "message": data.get('message'),
                    "data": data.get('data')
                }
            else:
                return {
                    "status": "FAILED",
                    "message": message,
                }


    def user_success_response(self, data=None, message=None):
        if data == None and message == None:
            return {
                "status": "SUCCESS",
                "message": "Success",
            }
        else:
            if data:
                return {
                    "status": "SUCCESS",
                    "message": data.get('message'),
                    "data": data.get('data')
                }
            else:
                return {
                    "status": "SUCCESS",
                    "message": message,
                }

u_responses = UserResponses()


