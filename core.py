from youtube_dl import YoutubeDL
from shutil import move as move_file
from moviepy.editor import VideoFileClip


def download_video(video_url: str):
    ret = {}
    with YoutubeDL() as ydl:
        # ret = ydl.download([video_url])
        try:
            dl_ret = ydl.extract_info(video_url, download=True)
            ret['id'], ret['title'], ret['ext'], ret['status'] = dl_ret['id'], dl_ret['title'], dl_ret['ext'], 1
        except Exception as e:
            ret['status'] = 0
    return ret


def extract_audio_from_video(video_path: str, audio_path: str) -> dict:
    info = {
        'desc': "",
        'is_success': False,
    }
    try:
        video = VideoFileClip(video_path)
    except:
        info['desc'] = "Can't read video file!"
        return info
    audio = video.audio
    try:
        audio.write_audiofile(audio_path)
        info['is_success'] = True
        return info
    except:
        info['desc'] = "Can't save audio file!"
        return info


if __name__ == "__main__":
    download_video('https://www.bilibili.com/video/BV1dt4y1i7sJ')
