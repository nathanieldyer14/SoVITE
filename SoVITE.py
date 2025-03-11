import srt
from moviepy import VideoFileClip, concatenate_videoclips
from datetime import timedelta

FPS = 25
RESOLUTION = (640,360)
SUBTITLE_SPEED = 1.5
NON_SUBTITLE_SPEED = 3

def speed_up_mp4(title=None, mp4_input=None, srt_input=None, subtitle_offset=0, subtitle_speed=SUBTITLE_SPEED, non_subtitle_speed=NON_SUBTITLE_SPEED, resolution=RESOLUTION, fps=FPS, mp4_output=None, threads=0):
    """
    Speed up an MP4 at different speeds for dialog vs. non-dialog using an SRT

    :param title: The filename of both .mp4 and .srt input filenames if the same else None
    :type title: str or None
    :param mp4_input: The filename of the input .mp4 file including the file extension. Can be None if title parameter is used
    :type mp4_input: str or None
    :param srt_input: The filename of the input .srt file including the file extension. Can be None if title parameter is used
    :type srt_input: str or None
    :param int subtitle_offset: The number of seconds faster the mp4 is than the subtitles. Default: 0
    :param subtitle_speed: The speedup factor for dialog/subtitle scenes. Default: 1.5
    :type subtitle_speed: int or float
    :param subtitle_speed: The speedup factor for non-dialog/non-subtitle scenes. Default: 3
    :type subtitle_speed: int or float
    :param resolution: The desired output mp4 resolution as a tuple of ints. Default: (640,360)
    :type resolution: (int,int)
    :param int fps: The desired output mp4 frames per second. Default: 25
    :param mp4_output: The filename for the output .mp4 file including the file extension. Can be None for Default: "faster\_" + `mp4_input`
    :type mp4_output: str or None
    :param int threads: The number of threads to run video processing with. Default: 0 for max threads
    :rtype: None
    :raises ValueError: if title is None while either input filename is None
    """
    if title is None and mp4_input is None:
        raise ValueError("mp4_input must not be None if title is None")
    if title is None and srt_input is None:
        raise ValueError("srt_input must not be None if title is None")
    if mp4_input is None:
        mp4_input = title + ".mp4"
    if srt_input is None:
        srt_input = title + ".srt"
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
    """
    Speed up an MP4 and SRT at different speeds for dialog vs. non-dialog using an SRT

    :param srt_input: The filename of the input .srt file including the file extension. Can be None if title parameter is used
    :type srt_input: str or None
    :param int subtitle_offset: The number of seconds faster the mp4 is than the subtitles. Default: 0
    :param subtitle_speed: The speedup factor for dialog/subtitle scenes. Default: 1.5
    :type subtitle_speed: int or float
    :param subtitle_speed: The speedup factor for non-dialog/non-subtitle scenes. Default: 3
    :type subtitle_speed: int or float
    :param srt_output: The filename for the output .srt file including the file extension. Can be None for Default: "faster\_" + `srt_input`
    :type srt_output: str or None
    :rtype: None
    """
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
    """
    Speed up an MP4 and SRT at different speeds for dialog vs. non-dialog using an SRT

    :param title: The filename of both .mp4 and .srt input filenames if the same else None
    :type title: str or None
    :param mp4_input: The filename of the input .mp4 file including the file extension. Can be None if title parameter is used
    :type mp4_input: str or None
    :param srt_input: The filename of the input .srt file including the file extension. Can be None if title parameter is used
    :type srt_input: str or None
    :param int subtitle_offset: The number of seconds faster the mp4 is than the subtitles. Default: 0
    :param subtitle_speed: The speedup factor for dialog/subtitle scenes. Default: 1.5
    :type subtitle_speed: int or float
    :param subtitle_speed: The speedup factor for non-dialog/non-subtitle scenes. Default: 3
    :type subtitle_speed: int or float
    :param resolution: The desired output mp4 resolution as a tuple of ints. Default: (640,360)
    :type resolution: (int,int)
    :param int fps: The desired output mp4 frames per second. Default: 25
    :param mp4_output: The filename for the output .mp4 file including the file extension. Can be None for Default: "faster\_" + `mp4_input`
    :type mp4_output: str or None
    :param srt_output: The filename for the output .srt file including the file extension. Can be None for Default: "faster\_" + `srt_input`
    :type srt_output: str or None
    :param int threads: The number of threads to run video processing with. Default: 0 for max threads
    :rtype: None
    :raises ValueError: if title is None while either input filename is None
    """
    if mp4_input is None:
        mp4_input = title + ".mp4"
    if srt_input is None:
        srt_input = title + ".srt"
    speed_up_srt(srt_input, subtitle_offset=subtitle_offset, subtitle_speed=subtitle_speed, non_subtitle_speed=non_subtitle_speed, srt_output=srt_output)
    speed_up_mp4(mp4_input=mp4_input, srt_input=srt_input, subtitle_offset=subtitle_offset, subtitle_speed=subtitle_speed, non_subtitle_speed=non_subtitle_speed, resolution=resolution, fps=fps, mp4_output=mp4_output, threads=threads)


if __name__ == "__main__":
    # speed_up_both(title="commissar")
    speed_up_both(title="gafnh", subtitle_offset=9)


