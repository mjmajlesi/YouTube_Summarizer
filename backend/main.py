from fastapi import FastAPI
from pydantic import BaseModel
from transcript import getTranscript , summary , extract_video_id


app = FastAPI()


class SummarizeRequest(BaseModel):
    url : str


@app.get("/")
def root():
    return {"massage": "Backend is running"}


@app.post("/summarize")
def summarize(request : SummarizeRequest):
    video_id = extract_video_id(request.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    text = getTranscript(video_id)
    summary_text = summary(text)
    return {"summary": summary_text}