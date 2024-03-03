import sys
import os
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_audioclips

def download_videos(singer_name, num_videos):
    os.makedirs("downloads", exist_ok=True)
    search_query = singer_name + " songs"
    search_results = YouTube.search(search_query, max_results=num_videos)
    for result in search_results:
        video_url = "https://www.youtube.com/watch?v=" + result.video_id
        video = YouTube(video_url)
        video_stream = video.streams.filter(file_extension="mp4", progressive=True).first()
        video_stream.download(output_path="downloads")

def convert_to_audio():
    for filename in os.listdir("downloads"):
        if filename.endswith(".mp4"):
            video = VideoFileClip(os.path.join("downloads", filename))
            audio = video.audio
            audio.write_audiofile(os.path.join("downloads", f"{filename[:-4]}.mp3"))
            video.close()
            audio.close()
            os.remove(os.path.join("downloads", filename))

def cut_audio(audio_duration):
    for filename in os.listdir("downloads"):
        if filename.endswith(".mp3"):
            audio = AudioFileClip(os.path.join("downloads", filename))
            audio = audio.subclip(0, audio_duration)
            audio.write_audiofile(os.path.join("downloads", filename))
            audio.close()

def merge_audios(output_filename):
    audio_clips = []
    for filename in os.listdir("downloads"):
        if filename.endswith(".mp3"):
            audio_clips.append(AudioFileClip(os.path.join("downloads", filename)))
    final_clip = concatenate_audioclips(audio_clips)
    final_clip.write_audiofile(output_filename)
    for clip in audio_clips:
        clip.close()
    final_clip.close()

def mashup(singer_name, num_videos, audio_duration, output_filename):
    try:
        download_videos(singer_name, num_videos)
        convert_to_audio()
        cut_audio(audio_duration)
        merge_audios(output_filename)
        print("Mashup completed successfully!")
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python 102103470.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer_name = sys.argv[1]
    num_videos = int(sys.argv[2])
    audio_duration = int(sys.argv[3])
    output_filename = sys.argv[4]

    mashup(singer_name, num_videos, audio_duration, output_filename)
