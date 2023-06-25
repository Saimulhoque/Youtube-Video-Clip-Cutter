import os
from pytube import YouTube
from moviepy.editor import VideoFileClip


def get_video_title(url):
    try:
        yt = YouTube(url)
        video_title = yt.title
        return video_title.strip() 
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def create_folder(path, folder_name):
    try:
        valid_characters = [c if c.isalnum() or c in [' ', '-', '_'] else '' for c in folder_name]
        folder_name = ''.join(valid_characters).strip()
        folder_path = os.path.join(path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def download_video(url, output, new_filename):
    try:
        video = YouTube(url)
        video_name = video.title
        print(f"File Name: " +video_name)

        stream = video.streams.get_highest_resolution()
        
        print(f"Downloading: " +video_name)

        video_filepath = stream.download(output)
        
        print("Video downloaded successfully!")
        
        # Clip the video into 1-minute segments
        clip_into_segments(video_filepath, output, video_name)
        
        print("Video clipped into 1-minute segments!")
    
    except Exception as e:
        print("An error occurred while processing the video:", str(e))


def clip_into_segments(filepath, output_directory, name,  duration=60):
    try:
        video = VideoFileClip(filepath)
        video_duration = video.duration
    
        num_segments = int(video_duration // duration)
        
        for i in range(num_segments):
            start_time = i * duration
            end_time = (i + 1) * duration
            output_filepath = os.path.join(output_directory, f"clip_{i+1}.mp4")
            video_segment = video.subclip(start_time, end_time)
            video_segment.write_videofile(output_filepath, codec="libx264", audio_codec="aac")
            video.close()
        print("Video clipped into 1-minute segments successfully!")
    except Exception as e:
        print("An error occurred while clipping the video:", str(e))





video_url = "https://youtu.be/G0S2xMfLg4M"  
output_directory = "Youtube"

video_title = get_video_title(video_url)

new_filename = video_title  

folder = create_folder(output_directory, video_title)  

if folder:
    print(f"Folder created: {folder}")
    download_video(video_url, folder, video_title)    
else:
    print("Failed to create folder.")

# download_video(video_url, output_directory, new_filename)