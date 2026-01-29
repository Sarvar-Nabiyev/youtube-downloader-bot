from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
import os
import asyncio
from downloader import get_video_info, download_video
from keyboards import create_quality_keyboard
from bot import user_data # In a real app, use a database or state

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\nMenga YouTube video linkini yuboring, men uni yuklab beraman.")

@router.message(F.text)
async def youtube_link_handler(message: types.Message) -> None:
    url = message.text.strip()
    if "youtube.com" not in url and "youtu.be" not in url:
        await message.answer("Iltimos, to'g'ri YouTube linkini yuboring.")
        return

    wait_msg = await message.answer("Video tahlil qilinmoqda... ⏳")
    
    info = await asyncio.to_thread(get_video_info, url)
    if not info:
        await wait_msg.edit_text("Videoni topib bo'lmadi yoki xatolik yuz berdi. 😔")
        return

    video_id = info.get('id')
    title = info.get('title')
    user_data[video_id] = {'url': url, 'title': title}
    
    keyboard = create_quality_keyboard(video_id, info.get('formats'))
    
    await wait_msg.edit_text(f"📹 <b>{title}</b>\n\nFormatni tanlang:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("down_"))
async def download_callback_handler(callback: types.CallbackQuery):
    data = callback.data.split("_")
    video_id = data[1]
    mode = data[2] # 'res' or 'audio'
    
    if video_id not in user_data:
        await callback.message.answer("Eskirgan so'rov. Iltimos, linkni qayta yuboring.")
        await callback.answer()
        return

    url = user_data[video_id]['url']
    title = user_data[video_id]['title']
    
    format_id = 'audio'
    if mode == 'res':
        res = data[3]
        # format string for yt-dlp to get specific resolution
        format_id = f"bestvideo[height<={res}]+bestaudio/best[height<={res}]"
        status_text = f"📹 {res}p video yuklanmoqda... ⏳"
    else:
        status_text = "🎵 Audio yuklanmoqda... ⏳"

    await callback.message.edit_text(status_text)
    
    # Download
    file_path = await asyncio.to_thread(download_video, url, format_id)
    
    if not file_path or not os.path.exists(file_path):
        await callback.message.edit_text("Yuklashda xatolik yuz berdi. 😔")
        return

    # Upload
    await callback.message.edit_text("Telegramga yuklanmoqda... 📤")
    
    try:
        if mode == 'audio':
            await callback.message.answer_audio(FSInputFile(file_path), caption=title)
        else:
            await callback.message.answer_video(FSInputFile(file_path), caption=title)
        
        await callback.message.delete()
    except Exception as e:
        await callback.message.answer(f"Fayl juda katta yoki xatolik: {e}")
    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

