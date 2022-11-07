import datetime as dt
import os
from math import floor

from PIL import Image
import shortuuid


def allowed_file(filename, exeptions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in exeptions


def save_image(file, path):
    name = '.'.join(file.filename.split('.')[:-1])
    ext = file.filename.split('.')[-1]
    print(ext)
    filename = f'{shortuuid.uuid()}_{dt.date.today().isoformat()}_{name}'
    file.save(os.path.join(path, f'{filename}.{ext}'))
    return name, ext, filename


def save_resize_image(filename, ext, path):
    resize_filename = f'{filename}_TN.{ext}'
    image = Image.open(os.path.join(path, f'{filename}.{ext}'))
    width, height = image.size
    ratio = (height / width)
    new_height = ratio * 500
    # print(new_height, ratio, width, height)
    resize_image = image.resize((500, floor(new_height)))
    print(resize_filename)
    resize_image.save(os.path.join(path, resize_filename))
    return resize_filename
