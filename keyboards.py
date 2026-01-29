from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_quality_keyboard(video_id, formats):
    builder = InlineKeyboardBuilder()
    
    # Filter and group formats (simplified logic for demonstration)
    # We want to show unique resolutions and an audio option
    
    resolutions = set()
    available_formats = []

    # Sort formats by resolution (height) in descending order
    # yt-dlp formats are usually a list of dicts. 
    # We are looking for video streams that have both video and audio, or we might need to merge.
    # For simplicity in this bot, let's look for 'best' pre-merged or handle merging if ffmpeg is available.
    # Assuming ffmpeg is installed, yt-dlp can merge. 
    
    # Let's pick a few standard qualities to show if available
    target_resolutions = [1080, 720, 480, 360]
    
    # We will pass format_id for video+audio. 
    # Note: yt-dlp 'bestvideo+bestaudio' is default but we want specific resolution.
    # format_id: f"bestvideo[height<={res}]+bestaudio/best[height<={res}]"
    
    for res in target_resolutions:
         builder.button(text=f"📹 {res}p", callback_data=f"down_{video_id}_res_{res}")
    
    builder.button(text="🎵 MP3 (Audio)", callback_data=f"down_{video_id}_audio")
    
    builder.adjust(2) # 2 buttons per row
    return builder.as_markup()
