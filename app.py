from flask import Flask, request, send_file
import subprocess, uuid, os

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_video():
    file = request.files['video']
    filename = str(uuid.uuid4()) + ".mp4"

    input_path = f"/tmp/{filename}"
    output_path = f"/tmp/out_{filename}"

    file.save(input_path)

    cmd = f'''
    ffmpeg -y -i "{input_path}" -filter_complex "
    [0:v]scale=1080:1920:flags=lanczos,
    eq=contrast=1.08:brightness=0.03:saturation=1.15,
    unsharp=5:5:1.2:5:5:0.0,
    boxblur=5:2[bg];
    [0:v]scale=920:-2:flags=lanczos,
    unsharp=5:5:1.0[fg];
    [bg][fg]overlay=(W-w)/2:(H-h)/2
    " -r 30 -c:v libx264 -preset fast -crf 23 -c:a copy "{output_path}"
    '''

    subprocess.run(cmd, shell=True)

    return send_file(output_path, as_attachment=True)

app.run(host="0.0.0.0", port=8080)