from fastapi import Header

class JwtAuth:
    def __init__(self):
        self.token = 'token-top'

    async def verify_token(self, token: str = Header('token')):
        print(token)
        return True
