from pydantic import BaseModel, EmailStr
from typing import List


class EmailSchema(BaseModel):
    """
    Schema used for emails sending. The schema is used in app/email.py.
    """
    email: List[EmailStr]
