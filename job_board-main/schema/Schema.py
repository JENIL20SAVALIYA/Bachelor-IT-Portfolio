from pydantic import BaseModel,field_validator,Field,EmailStr


class Job(BaseModel):
    title:str
    description:str
    salary : float = Field(...,gt=0)

    @field_validator("title")
    def check_title(cls,v):
        if not v :
            raise ValueError("Title must not be empty")
        
        return v
    
class User(BaseModel):
    username:str
    email : EmailStr
    password:str
    
    @field_validator("username")
    def check_username(cls,v):
        if not v :
            raise ValueError("username must not empty")
        
        return v

    
    @field_validator("password")
    def check_password(cls,v):
        if len(v) < 8:
            raise ValueError("password length must be 8 or more")
        
        return v
