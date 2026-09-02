import re
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str):
    parsed = urlparse(url)
    host = parsed.netloc.lower()

    if "youtu.be" in host:
        video = parsed.path.lstrip("/").split("/")[0]
        return video or None

    if "youtube.com" in host:
        if parsed.path.startswith("/shorts/"):
            video = parsed.path.split("/shorts/")[1].split("/")[0]
            return video or None

        qs = parse_qs(parsed.query)
        video = qs.get("v", [None])[0]
        return video

    return None


def getTranscript(video_id: str):
    ytt_api = YouTubeTranscriptApi()
    # ponytail: preferred fa→en covers 99% of your audience; full fallback below is the ceiling
    try:
        fetched = ytt_api.fetch(video_id, languages=["fa", "en"])
        return " ".join([t.text for t in fetched])
    except Exception:
        pass

    transcript_list = ytt_api.list(video_id)
    try:
        transcript = transcript_list.find_transcript(["fa", "en"])
    except Exception:
        try:
            transcript = next(iter(transcript_list))
        except StopIteration:
            raise Exception("No transcripts available for this video")
    fetched = transcript.fetch()
    return " ".join([t.text for t in fetched])


def summary(text: str, maxLen: int = 5) -> str:
    """Extractive summary via TF-IDF: score each sentence by sum of TF-IDF weights, pick top-k in original order."""
    text = text.strip()
    if not text:
        return ""

    sentences = [s.strip() for s in re.split(r"(?<=[.!?؟])\s+", text) if s.strip()]
    if len(sentences) <= maxLen:
        return " ".join(sentences)

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        import numpy as np
    except ImportError:
        # ponytail: install scikit-learn for real TF-IDF
        return " ".join(sentences[:maxLen])

    for stop in ("english", None):
        try:
            vectorizer = TfidfVectorizer(stop_words=stop)
            tfidf = vectorizer.fit_transform(sentences)
            break
        except ValueError:
            continue
    else:
        return " ".join(sentences[:maxLen])

    scores = np.asarray(tfidf.sum(axis=1)).ravel()
    top = sorted(np.argsort(scores)[-maxLen:])
    return " ".join(sentences[i] for i in top)
