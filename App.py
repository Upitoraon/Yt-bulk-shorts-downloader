from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/get_shorts", methods=["GET"])
def get_shorts():
    channel_url = request.args.get("channel_url")

    result = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--print", "%(url)s", channel_url],
        capture_output=True,
        text=True,
    )

    video_urls = result.stdout.strip().split("\n")
    shorts_list = [url for url in video_urls if "shorts" in url]

    return jsonify(shorts_list)

@app.route("/download", methods=["POST"])
def download():
    url = request.json.get("url")

    subprocess.run(
        [
            "yt-dlp",
            "-f",
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "-o",
            "/sdcard/Downloads/%(title)s.mp4",
            url,
        ]
    )

    return jsonify({"status": "Download Started!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
