from pydantic import BaseModel


class NegativeSentiment(BaseModel):
    is_negative_word :bool

class UserInfo(BaseModel):
    name :str
    age :str