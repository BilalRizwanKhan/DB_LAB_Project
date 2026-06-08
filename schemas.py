from pydantic import BaseModel

class SignupSchema(BaseModel):
    name: str
    email: str
    password: str

class LoginSchema(BaseModel):
    email: str
    password: str

class PropertySchema(BaseModel):
    title: str
    location: str
    price: int
    description: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    name: str

class ReviewSchema(BaseModel):
    rating:  int    # 1-5
    comment: str

class InquirySchema(BaseModel):
    message: str

class InquiryReplySchema(BaseModel):
    reply: str

class ProfileUpdateSchema(BaseModel):
    name:  str
    phone: str = None
    city:  str = None
    bio:   str = None

class PasswordChangeSchema(BaseModel):
    current_password: str
    new_password:     str

class AppointmentSchema(BaseModel):
    visit_date: str
    visit_time: str
    note:       str = None
