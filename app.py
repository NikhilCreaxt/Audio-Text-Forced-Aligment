from flask import Flask, request, jsonify
from forcealign import ForceAlign
import os

app = Flask(__name__)

@app.route("/align", methods=["POST"])
def align_audio():
    # Get the uploaded file and transcript
    if "audio" not in request.files or "transcript" not in request.form:
        return jsonify({"error": "Missing audio or transcript"}), 400

    audio_file = request.files["audio"]
    transcript = request.form["transcript"]

    # Save audio to a temp file
    audio_path = "temp.wav"
    audio_file.save(audio_path)

    try:
        # Run alignment
        aligner = ForceAlign(audio_file=audio_path, transcript=transcript)
        words = aligner.inference()

        # Format output
        result = {
            "alignment": [
                {
                    "word": w.word,
                    "start": round(w.time_start, 3),
                    "end": round(w.time_end, 3)
                }
                for w in words
            ]
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

# ✅ Run with dynamic Render port
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 10000))  # Get port from Render
#     app.run(host="0.0.0.0", port=port, debug=True)