# Summary
This script uses an SRT subtitle/caption file to speed up a corresponding mp4 to different speeds for dialog and non-dialog scenes. 

This is most useful for watching videos, particularly slow-paced Soviet/foreign films, quickly without skipping anything while keeping dialog understandable / subtitles readable.

# Project Name Explanation
"vite" => "fast" in French

"So VITE" => "So FAST"

"SoVITE" ~ "Soviet" (works well on Soviet films b/c they often have subtitles and slow non-dialog scenes)

# How to Download YouTube MP4 & SRT
0. run `pip install yt-dlp` if you haven't before
1. run `yt-dlp <YouTube link>` to download mp4
2. add `subtitle.to/` before YouTube url 
3. download SRT format subtitles in desired language
4. if desired language not found, try searching subtitle websites, like `www.opensubtitles.org`
5. if using 3rd-party subtitles, open the SRT and compare the first start time with mp4's to find `subtitle_offset`
