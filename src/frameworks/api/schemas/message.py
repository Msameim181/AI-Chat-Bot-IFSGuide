from pydantic import BaseModel
from typing import Union

class CreateMessage(BaseModel):
    interaction_id: Union[str, int]
    content: str


class FetchAllMessages(BaseModel):
    interaction_id: Union[str, int]
