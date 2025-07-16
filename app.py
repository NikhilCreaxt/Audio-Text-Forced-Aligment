from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from forcealign import ForceAlign
import os
import uvicorn

app = FastAPI()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use PORT from environment or default to 8000
    uvicorn.run("app:app", host="0.0.0.0", port=port)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/align")
async def align_audio(
    audio: UploadFile = File(...),
    transcript: str = Form(...)
):
    # Save uploaded audio
    audio_path = "temp.wav"
    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    # Run alignment
    aligner = ForceAlign(audio_file=audio_path, transcript=transcript)
    words = aligner.inference()

    # Clean up temp audio
    os.remove(audio_path)

    # Format response
    return {
        "alignment": [
            {
                "word": w.word,
                "start": round(w.time_start, 3),
                "end": round(w.time_end, 3)
            }
            for w in words
        ]
    }