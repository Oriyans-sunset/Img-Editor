from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont
import base64, io

def rotate_img(pic, angle):
    img_obj = Image.open(io.BytesIO(pic))
    rotated_img = img_obj.rotate(int(angle))
    data = io.BytesIO()
    rotated_img.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue()).decode("utf-8")

    return encoded_img_data

def black_and_white_img(pic):
    img_obj = Image.open(io.BytesIO(pic))
    rotated_img = img_obj.convert("L")
    data = io.BytesIO()
    rotated_img.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue()).decode("utf-8")

    return encoded_img_data

def flip_img(pic):
    img_obj = Image.open(io.BytesIO(pic))
    rotated_img = img_obj.transpose(Image.FLIP_TOP_BOTTOM)
    data = io.BytesIO()
    rotated_img.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue()).decode("utf-8")

    return encoded_img_data

def blur_img(pic, amt):
    img_obj = Image.open(io.BytesIO(pic))
    blur_image = img_obj.filter(ImageFilter.BoxBlur(int(amt)))
    data = io.BytesIO()
    blur_image.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue()).decode("utf-8")

    return encoded_img_data

def smooth_img(pic):
    img_obj = Image.open(io.BytesIO(pic))
    smooth_image = img_obj.filter(ImageFilter.SMOOTH)
    data = io.BytesIO()
    smooth_image.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue()).decode("utf-8")

    return encoded_img_data

def sharp_img(pic):
    img_obj = Image.open(io.BytesIO(pic))
    sharp_image = img_obj.filter(ImageFilter.SHARPEN)
    data = io.BytesIO()
    sharp_image.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue()).decode("utf-8")

    return encoded_img_data

def edge_detection(pic):
    img_obj = Image.open(io.BytesIO(pic))
    img_gray = img_obj.convert("L")
    img_gray_smooth = img_gray.filter(ImageFilter.SMOOTH)
    edges_smooth = img_gray_smooth.filter(ImageFilter.FIND_EDGES)
    data = io.BytesIO()
    edges_smooth.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue()).decode("utf-8")

    return encoded_img_data

def emboss_img(pic):
    img_obj = Image.open(io.BytesIO(pic))
    img_gray = img_obj.convert("L")
    img_gray_smooth = img_gray.filter(ImageFilter.SMOOTH)
    emboss_image = img_gray_smooth.filter(ImageFilter.EMBOSS)
    data = io.BytesIO()
    emboss_image.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue()).decode("utf-8")

    return encoded_img_data

def contrast_img(pic, amt):
    img_obj = Image.open(io.BytesIO(pic))
    filter = ImageEnhance.Contrast(img_obj)
    enhanced_img = filter.enhance(float(amt))
    data = io.BytesIO()
    enhanced_img.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue()).decode("utf-8")

    return encoded_img_data

def bright_img(pic, amt):
    img_obj = Image.open(io.BytesIO(pic))
    filter = ImageEnhance.Brightness(img_obj)
    bright_img = filter.enhance(float(amt))
    data = io.BytesIO()
    bright_img.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue()).decode("utf-8")

    return encoded_img_data

def add_border(pic, color, border_width):
    img_obj = Image.open(io.BytesIO(pic))
    border = (border_width, border_width, border_width, border_width)
    border_img = ImageOps.expand(img_obj, border=border, fill=color)
    data = io.BytesIO()
    border_img.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue()).decode("utf-8")

    return encoded_img_data

def add_caption(pic, color, text):
    img_obj = Image.open(io.BytesIO(pic))

    border = (40, 40, 40, 50)
    border_img = ImageOps.expand(img_obj, border=border, fill="white")

    W, H = border_img.size

    d1 = ImageDraw.Draw(border_img)
    myFont = ImageFont.truetype("/app/static/permanent.marker.regular.ttf", 40)
    d1.text((10, H/1.09), text, font=myFont, fill=color)

    data = io.BytesIO()
    border_img.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue()).decode("utf-8")

    return encoded_img_data
