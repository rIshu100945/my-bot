from flask import Flask, request, send_file, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)

# -----------------------------
# Ensure FFmpeg is available
# -----------------------------
def setup_ffmpeg():
    if not os.path.exists("ffmpeg"):
        print("FFmpeg not found, downloading...")

        os.system("apt-get update && apt-get install -y wget xz-utils")

        os.system("wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz")
        os.system("tar -xf ffmpeg-release-amd64-static.tar.xz")
        os.system("cp ffmpeg-*-static/ffmpeg ./ffmpeg")
        os.system("chmod +x ffmpeg")

        print("FFmpeg downloaded ✅")

    return "./ffmpeg"

FFMPEG_PATH = setup_ffmpeg()

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return "API running ✅"

@app.route("/process", methods=["POST"])
def process_video():
    try:
        file = request.files.get("video")

        if not file:
            return jsonify({"error": "No file"}), 400

        # Unique filenames
        filename = str(uuid.uuid4()) + ".mp4"
        input_path = f"/tmp/{filename}"
        output_path = f"/tmp/out_{filename}"

        file.save(input_path)

        # FFmpeg command (simple re-encode)
        cmd = [
            FFMPEG_PATH,
            "-i", input_path,
            "-vcodec", "libx264",
            "-acodec", "aac",
            output_path
        ]

        subprocess.run(cmd, check=True)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
