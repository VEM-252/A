import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch # Correct import
from config import YOUTUBE_IMG_URL

# Helper function for resizing
def resize_image(image, width, height):
    return image.resize((width, height), Image.LANCZOS)

# Function name changed to gen_thumb to fix ImportError
async def gen_thumb(videoid):
    cache_path = f"cache/{videoid}.png"
    temp_path = f"cache/thumb{videoid}.png"
    
    if os.path.isfile(cache_path):
        return cache_path

    if not os.path.exists("cache"):
        os.makedirs("cache")

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        res_data = await results.next()
        
        if not res_data["result"]:
            return YOUTUBE_IMG_URL

        result = res_data["result"][0]
        title = re.sub(r"\W+", " ", result.get("title", "Unsupported Title")).title()
        duration = result.get("duration", "Unknown")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        views = result.get("viewCount", {}).get("short", "Unknown Views")

        # Download thumbnail
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(temp_path, mode="wb") as f:
                        await f.write(await resp.read())

        # Image Processing
        youtube = Image.open(temp_path).convert("RGBA")
        
        GLOW_COLOR = "#ff0099" 
        BORDER_COLOR = "#FF1493"

        # Background
        bg = resize_image(youtube, 1280, 720)
        bg = bg.filter(ImageFilter.GaussianBlur(25))
        bg = ImageEnhance.Brightness(bg).enhance(0.3)

        # Main Thumbnail
        thumb_width, thumb_height = 840, 460
        main_thumb = resize_image(youtube, thumb_width, thumb_height)
        
        mask = Image.new("L", (thumb_width, thumb_height), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([(0, 0), (thumb_width, thumb_height)], radius=25, fill=255)
        main_thumb.putalpha(mask)

        center_x, center_y = 640, 320
        thumb_x = center_x - (thumb_width // 2)
        thumb_y = center_y - (thumb_height // 2)

        # Glow
        glow_layer = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
        draw_glow = ImageDraw.Draw(glow_layer)
        draw_glow.rounded_rectangle(
            [(thumb_x - 15, thumb_y - 15), (thumb_x + thumb_width + 15, thumb_y + thumb_height + 15)],
            radius=35, fill=GLOW_COLOR
        )
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(20))
        bg.paste(glow_layer, (0, 0), glow_layer)

        # Border
        border_layer = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
        draw_border = ImageDraw.Draw(border_layer)
        draw_border.rounded_rectangle(
            [(thumb_x - 5, thumb_y - 5), (thumb_x + thumb_width + 5, thumb_y + thumb_height + 5)],
            radius=30, fill=BORDER_COLOR
        )
        bg.paste(border_layer, (0, 0), border_layer)
        bg.paste(main_thumb, (thumb_x, thumb_y), main_thumb)

        draw = ImageDraw.Draw(bg)
        
        try:
            font_title = ImageFont.truetype("BIGFM/assets/font.ttf", 45)
            font_details = ImageFont.truetype("BIGFM/assets/font2.ttf", 30)
        except:
            font_title = ImageFont.load_default()
            font_details = ImageFont.load_default()

        if len(title) > 40:
            title = title[:37] + "..."

        # Draw Title and Stats
        draw.text((320, 580), title, fill="white", font=font_title)
        stats_text = f"Views: {views} | Duration: {duration}"
        draw.text((320, 640), stats_text, fill=BORDER_COLOR, font=font_details)

        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        bg.convert("RGB").save(cache_path, "PNG")
        return cache_path

    except Exception as e:
        print(f"Error: {e}")
        return YOUTUBE_IMG_URL

# Optional: keep this if needed by other files
async def get_qthumb(vidid):
    try:
        url = f"https://www.youtube.com/watch?v={vidid}"
        results = VideosSearch(url, limit=1)
        res_data = await results.next()
        return res_data["result"][0]["thumbnails"][0]["url"].split("?")[0]
    except Exception:
        return YOUTUBE_IMG_URL
