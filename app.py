from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# ✅ Check if FFmpeg is installed
def check_ffmpeg():
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("✅ FFMPEG INSTALLED")
        print(result.stdout.split("\n")[0])
    except Exception as e:
        print("❌ FFMPEG NOT FOUND:", e)

check_ffmpeg()

# ✅ Test route (very important)
@app.route("/")
def home():
    return "Server is running ✅"

# ✅ Example endpoint using FFmpeg
@app.route("/process", methods=["POST"])
def process_video():
    try:
        input_file = "input.mp4"
        output_file = "output.mp4"

        # Dummy example command (replace with your real logic)
        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_file,
            "-vf", "scale=640:360",
            output_file
        ]

        subprocess.run(cmd, check=True)

        return jsonify({
            "status": "success",
            "message": "Video processed"
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ✅ IMPORTANT: Railway dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    print(f"🚀 Running on port {port}")
    app.run(host="0.0.0.0", port=port)
