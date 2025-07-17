from pydantic import BaseModel, Field
from typing import List, Optional

class ChannelReport(BaseModel):
    channel_name: str = Field(..., description="Name of the Telegram channel", example="chemed")
    count: int = Field(..., description="Number of messages in the channel", example=120)

class ChannelActivity(BaseModel):
    channel_name: str = Field(..., description="Name of the Telegram channel", example="lobelia4cosmetics")
    total_messages: int = Field(..., description="Total number of messages in the channel", example=200)
    messages_per_day: Optional[dict] = Field(None, description="Messages per day as a dictionary of date to count", example={"2024-07-10": 20, "2024-07-11": 30})

class MessageSearchResult(BaseModel):
    message_id: int = Field(..., description="Unique message identifier", example=123)
    channel_name: str = Field(..., description="Name of the Telegram channel", example="chemed")
    date: str = Field(..., description="Date of the message", example="2024-07-10")
    text: str = Field(..., description="Message text", example="Paracetamol available now!") 