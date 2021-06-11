from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO

def make(input="template.png", qrcode="qrcode.png", output="grabber.png", size=314):
    wanted = Image.open(input)
    pfp = Image.open(qrcode)
    pfp = pfp.resize((size,size))
    wanted.paste(pfp, (200,720))
    draw = ImageDraw.Draw(wanted)
    wanted.save(output)