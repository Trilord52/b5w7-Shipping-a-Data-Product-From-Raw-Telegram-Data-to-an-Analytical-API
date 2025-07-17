from fastapi import FastAPI, Query, HTTPException
from typing import List
from .schemas import ChannelReport, ChannelActivity, MessageSearchResult
from .crud import get_top_channels, get_channel_activity, search_messages
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Telegram Medical Analytics API", description="Analytical API for Telegram medical business data.")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Telegram Medical Analytics API!"}

@app.get("/api/reports/top-channels", response_model=List[ChannelReport], tags=["Reports"])
def api_top_channels(limit: int = Query(10, ge=1, le=100)):
    """Get the most active channels by message count."""
    return get_top_channels(limit)

@app.get("/api/channels/{channel_name}/activity", response_model=ChannelActivity, tags=["Channels"])
def api_channel_activity(channel_name: str):
    """Get posting activity for a specific channel."""
    result = get_channel_activity(channel_name)
    if not result:
        raise HTTPException(status_code=404, detail="Channel not found")
    return result

@app.get("/api/search/messages", response_model=List[MessageSearchResult], tags=["Search"])
def api_search_messages(query: str = Query(..., min_length=1)):
    """Search for messages containing a specific keyword."""
    return search_messages(query) 