# ================= INSTALL =================
!pip install flask pyngrok
!apt-get install -y ffmpeg

# ================= IMPORTS =================
from flask import Flask, request, send_file
from pyngrok import ngrok
import subprocess, uuid

# 🔑 ADD YOUR NGROK TOKEN HERE
!ngrok config add-authtoken 3CeljREva1Izw11UxgY1I3piOQ0_2enXKJ4mgXocbGy69B9pL

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_video():
    file = request.files['video']

    filename = str(uuid.uuid4()) + ".mp4"
    input_path = f"/content/{filename}"
    output_path = f"/content/out_{filename}"

    # save uploaded video
    file.save(input_path)

    # 🔥 FFmpeg processing (your effect)
    cmd = f'''
    ffmpeg -y -i "{input_path}" -filter_complex "[0:v]scale=1080:1920:flags=lanczos,eq=contrast=1.08:brightness=0.03:saturation=1.15,unsharp=5:5:1.2:5:5:0.0,boxblur=5:2[bg];[0:v]scale=920:-2:flags=lanczos,unsharp=5:5:1.0[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -r 30 -s 1080x1920 -c:v libx264 -preset fast -crf 18 -c:a copy "{output_path}"
    '''

    subprocess.run(cmd, shell=True)

    return send_file(output_path, as_attachment=True)

# ================= NGROK =================
ngrok.kill()
public_url = ngrok.connect(5000)
print("🔥 YOUR API URL:", public_url)

# ================= RUN =================
app.run(port=5000)
