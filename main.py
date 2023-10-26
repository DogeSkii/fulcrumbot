# get outa here you nosey fucker
# i mean you can look at the code but like
# don't fuck up my precious hacky code :)))

# doge.com was here
# doge.com made this
# doge.com will be sad if you fuck this up
# i am
# doge.com
import yt_dlp as ydl
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import shutil

def read_video_url_from_file(filename):
    with open(filename, "r") as file:
        return file.readline().strip()

def download_youtube_video(video_url, output_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
    }
    with ydl.YoutubeDL(ydl_opts) as ydl_instance:
        ydl_instance.download([video_url])

def split_video(video_path, output_folder, split_duration=60):
    video_clip = VideoFileClip(video_path)
    total_duration = video_clip.duration
    current_time = 0
    part_number = 1
    split_files = []

    while current_time < total_duration:
        start_time = current_time
        end_time = current_time + split_duration
        if end_time > total_duration:
            end_time = total_duration

        part_filename = os.path.join(output_folder, f"part_{part_number}.mp4")
        subclip = video_clip.subclip(start_time, end_time)
        subclip.write_videofile(part_filename, codec="libx264")

        split_files.append(part_filename)

        current_time = end_time
        part_number += 1

    video_clip.close()
    return split_files

def delete_and_rearrange(output_folder, split_files):
    if len(split_files) < 2:
        print("Insufficient split files to rearrange.")
        return

    os.remove(split_files[0])  # Delete the first split file

    temp_folder = os.path.abspath("temp")
    os.makedirs(temp_folder, exist_ok=True)

    for i, filename in enumerate(split_files[1:]):
        new_filename = os.path.join(temp_folder, f"reordered_part_{i+1}.mp4")
        shutil.copy(filename, new_filename)

    shutil.rmtree(output_folder)
    os.rename(temp_folder, output_folder)

def main():
    url_filename = "url.txt"
    output_folder = "output"
    output_path = os.path.join(output_folder, "video.mp4")

    # Read split_duration from file
    split_duration_filename = "duration.txt"
    if os.path.exists(split_duration_filename):
        with open(split_duration_filename, "r") as duration_file:
            split_duration = int(duration_file.read().strip())
    else:
        # Use a default value if the file doesn't exist
        split_duration = 60  # seconds

    os.makedirs(output_folder, exist_ok=True)
    video_url = read_video_url_from_file(url_filename)
    print("Video URL:")
    print(video_url)
    print("Split Length:")
    print(split_duration)
    input('press enter to cont \n')
    download_youtube_video(video_url, output_path)
    split_files = split_video(output_path, output_folder, split_duration)
    delete_and_rearrange(output_folder, split_files)

    print("Video downloaded, split, first clip deleted, and clips rearranged successfully!")

if __name__ == "__main__":
    main()