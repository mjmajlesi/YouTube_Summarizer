from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transcript import getTranscript, summary, extract_video_id


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SummarizeRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.post("/summarize")
def summarize(request: SummarizeRequest):
    video_id = extract_video_id(request.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    try:
        text = getTranscript(video_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    summary_text = summary(text)
    return {"summary": summary_text}
