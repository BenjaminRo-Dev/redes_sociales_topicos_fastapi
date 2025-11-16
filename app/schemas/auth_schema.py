from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Pa JWT:
class Token(object):
    access_token: str
    token_type: str = "bearer"