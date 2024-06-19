import os.path
from pytube import YouTube
from moviepy.editor import VideoFileClip

async def download_youtube_video_as_mp3(youtube_url):
    try:
        yt = YouTube(youtube_url)
        video_stream = yt.streams.filter(resolution="360p").first()
        video_title = yt.title
        mp3_filename = f"{video_title}.mp3"
        file_path = os.path.join("audio",mp3_filename)
        if os.path.exists(file_path):
            return file_path 
        
        else:
            download_path = video_stream.download()
            video_clip = VideoFileClip(download_path)
            video_clip.audio.write_audiofile(file_path,fps= 44100)
            video_clip.close()
            os.remove(download_path)
            print(f"Downloaded '{video_title}' successfully!")
            return mp3_filename

    except Exception as e:
        print(f"An error occurred: {e}")