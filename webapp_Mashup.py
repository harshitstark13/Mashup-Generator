from flask import Flask, render_template, request
import os
from pytube import YouTube
import zipfile

app = Flask(__name__)

def download_videos(singer_name, num_videos):
    os.makedirs("downloads", exist_ok=True)
    search_query = singer_name + " songs"
    search_results = YouTube.search(search_query, max_results=num_videos)
    for result in search_results:
        video_url = "https://www.youtube.com/watch?v=" + result.video_id
        video = YouTube(video_url)
        video_stream = video.streams.filter(file_extension="mp4", progressive=True).first()
        video_stream.download(output_path="downloads")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer_name = request.form["singer_name"]
        num_videos = int(request.form["num_videos"])
        audio_duration = int(request.form["audio_duration"])
        email = request.form["email"]
        output_filename = f"{singer_name.replace(' ', '_')}_mashup.zip"

        try:
            download_videos(singer_name, num_videos)
            # Convert videos to audio, cut audio, merge audios (not implemented in this example)
            # Compress files into a ZIP archive
            with zipfile.ZipFile(output_filename, 'w') as zipf:
                for filename in os.listdir("downloads"):
                    if filename.endswith(".mp4"):
                        zipf.write(os.path.join("downloads", filename), arcname=filename)
            # Send email with the ZIP file attachment (implementation not provided)
            return "Mashup completed! Check your email for the file."
        except Exception as e:
            return "An error occurred during mashup: " + str(e)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
