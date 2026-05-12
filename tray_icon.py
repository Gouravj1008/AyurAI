from PIL import Image, ImageDraw

img = Image.new("RGB", (64, 64), "#1DB954")
draw = ImageDraw.Draw(img)
draw.text((18, 18), "J", fill="black")
img.save("jarvis.ico")
