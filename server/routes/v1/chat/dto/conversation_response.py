from datetime import datetime
from pydantic import BaseModel

class ConversationResponse(BaseModel):
    user_id: int
    username: str
    last_message: str
    last_message_at: datetime
