"""FastAPI backend for the Tone Rewriter web app."""

import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from tone_rewriter.config import MODEL, TONES
from tone_rewriter.rewriter import rewrite_stream

app = FastAPI(title="Tone Rewriter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class RewriteRequest(BaseModel):
    text: str
    tone_key: str


@app.get("/api/tones")
def get_tones():
    return {
        "model": MODEL,
        "tones": [
            {"key": k, "name": name, "description": desc}
            for k, (name, desc) in TONES.items()
        ],
    }


@app.post("/api/rewrite")
def rewrite(body: RewriteRequest):
    if body.tone_key not in TONES:
        return {"error": "Invalid tone key"}

    _, tone_desc = TONES[body.tone_key]

    def event_stream():
        for chunk in rewrite_stream(body.text, tone_desc):
            yield f"data: {json.dumps({'token': chunk})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# Serve built frontend in production
try:
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
except Exception:
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
