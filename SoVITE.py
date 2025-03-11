import srt
from moviepy import VideoFileClip, concatenate_videoclips
from datetime import timedelta


# # # # # # # # # # # HOW TO DOWNLOAD YOUTUBE MP4 & SRT # # # # # # # # # # #
# 0. run `pip install yt-dlp` if you haven't before
# 1. run `yt-dlp <YouTube link>` to download mp4
# 2. add `subtitle.to/` before YouTube url 
# 3. download SRT format subtitles in desired language
# 4. if desired language not found, try searching subtitle websites, like `www.opensubtitles.org`
# 5. if using 3rd-party subtitles, open the SRT and compare the first start time with mp4's to find offset
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

FPS = 25
RESOLUTION = (640,360)
SUBTITLE_SPEED = 1.5
NON_SUBTITLE_SPEED = 3

def speed_up_mp4(mp4_input, srt_input, subtitle_offset=0, subtitle_speed=SUBTITLE_SPEED, non_subtitle_speed=NON_SUBTITLE_SPEED, resolution=RESOLUTION, fps=FPS, mp4_output=None, threads=0):
    if mp4_output is None:
        mp4_output = "faster_" + mp4_input
    
    clip = VideoFileClip(mp4_input).resized(resolution)
    with open(srt_input, "r") as f:
        srt_text = f.read()
        
    clips = []
    last_end = timedelta(0)
    td_subtitle_offset = timedelta(seconds=subtitle_offset)
    
    for subtitle in srt.parse(srt_text):
        subtitle.start += td_subtitle_offset
        subtitle.end += td_subtitle_offset
        subtitle_start, subtitle_end = str(subtitle.start), str(subtitle.end)
        clips.append(clip.subclipped(str(last_end.total_seconds()), subtitle_start).with_speed_scaled(non_subtitle_speed))  # Non-SUBTITLE segment
        clips.append(clip.subclipped(subtitle_start, subtitle_end).with_speed_scaled(subtitle_speed))  # SUBTITLE segment
        last_end = subtitle.end
    clips.append(clip.subclipped(str(last_end.total_seconds()), clip.duration).with_speed_scaled(non_subtitle_speed))  # Remaining normal-speed segment
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(mp4_output, fps=fps, threads=threads)
    
    
def speed_up_srt(srt_input, subtitle_offset=0, subtitle_speed=SUBTITLE_SPEED, non_subtitle_speed=NON_SUBTITLE_SPEED, srt_output=None):
    if srt_output is None:
        srt_output = "faster_" + srt_input
        
    # read subtitle file into string
    with open(srt_input, "r") as f:
        srt_text = f.read()
    
    
    last_end = timedelta(0)
    last_final_end = timedelta(0)
    td_subtitle_offset = timedelta(seconds=subtitle_offset)
    
    new_subtitles = []
    for subtitle in srt.parse(srt_text):
        # subtitle offset
        subtitle.start += td_subtitle_offset
        subtitle.end += td_subtitle_offset
        # calc durations
        pre_duration = (subtitle.start - last_end) / non_subtitle_speed
        duration = (subtitle.end - subtitle.start) / subtitle_speed
        # calc new start/end
        new_start = last_final_end + pre_duration
        new_end = last_final_end + pre_duration + duration
        # create and append new Subtitle object
        new_subtitles.append(srt.Subtitle(index=subtitle.index, start=new_start, end=new_end, content=subtitle.content, proprietary=subtitle.proprietary))
        # save ends for next iteration
        last_end = subtitle.end
        last_final_end = new_end
        
    # write new subtitles to file
    with open(srt_output, "w") as f:
        f.write(srt.compose(new_subtitles))
        

def speed_up_both(title=None, mp4_input=None, srt_input=None, subtitle_offset=0, subtitle_speed=SUBTITLE_SPEED, non_subtitle_speed=NON_SUBTITLE_SPEED, resolution=RESOLUTION, fps=FPS, mp4_output=None, srt_output=None, threads=0):
    if mp4_input is None:
        mp4_input = title + ".mp4"
    if srt_input is None:
        srt_input = title + ".srt"
    speed_up_srt(srt_input, subtitle_offset=subtitle_offset, subtitle_speed=subtitle_speed, non_subtitle_speed=non_subtitle_speed, srt_output=srt_output)
    speed_up_mp4(mp4_input, srt_input, subtitle_offset=subtitle_offset, subtitle_speed=subtitle_speed, non_subtitle_speed=non_subtitle_speed, resolution=resolution, fps=fps, mp4_output=mp4_output, threads=threads)


if __name__ == "__main__":
    # speed_up_both(title="commissar")
    speed_up_both(title="gafnh", subtitle_offset=9)


