class JWTResponses:

    def jwtauthsuccess(self, data):

        return {
            "status": "SUCCESS",
            "message": "Login successful",
            "access": data,
        }

    def jwtautherror(self, message=None):

        if message:
            return {
                "status": "FAILED",
                "message": message
            }
        else:
            return {
                "status": "FAILED",
                "message": "Incorrect login credentials, please check username and password and try again.",
            }
        
    def jwtlogoutsuccess(self):

        return {
            "status": "SUCCESS",
            "message": "Logout successful"
        }

xauth_responses = JWTResponses()
        