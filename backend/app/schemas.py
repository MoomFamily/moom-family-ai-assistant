from pydantic import BaseModel, EmailStr, Field
class RegisterIn(BaseModel): email: EmailStr; password: str = Field(min_length=12, max_length=128)
class LoginIn(BaseModel): email: EmailStr; password: str
class TokenOut(BaseModel): access_token: str; token_type: str = 'bearer'
class ConversationIn(BaseModel): title: str = Field(default='New conversation', max_length=200)
class MessageIn(BaseModel): content: str = Field(min_length=1, max_length=20000)
