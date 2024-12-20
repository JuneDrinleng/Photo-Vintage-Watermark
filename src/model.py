import json
import os
import cv2
from PIL import Image,ImageDraw, ImageFont
from PIL.ExifTags import TAGS
import sys
import numpy as np

status_code=0

def check_condition(value):
    if value !=0:
        print(f"Error code: {value}")
        sys.exit(1)  # 非零状态码表示程序异常终止
        
    else:
        pass

def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_image_date(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'DateTimeOriginal':
                    date=value.split(" ")[0]
                    time=value.split(" ")[1]
                    return [date,time]
        else:
            status_code=2
            return "No date information found" 
    except Exception as e:
        status_code=3
        return str(e)
    
def add_date_to_image(image_path, date_text,output_path,font_path):
    image = cv2.imread(image_path)
    if image is None:
        status_code=1
        check_condition(status_code)
        pass
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # font_scale = 10
    # font_color = (50, 108,255)  #b g r
    # thickness = 20
    # margin = 10


    # draw = ImageDraw.Draw(pil_image)
    # font = ImageFont.truetype(font_path, 40)  # 设置字体和大小

    # text_size, _ = cv2.getTextSize(date_text, font, font_scale, thickness)
    # text_width, text_height = text_size

    # x = image.shape[1] - text_width - margin
    # y = image.shape[0] - margin

    # cv2.putText(image, date_text, (x, y), font, font_scale, font_color, thickness)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)

    draw = ImageDraw.Draw(pil_image)
    font = ImageFont.truetype(font_path, pil_image.width/25)  # 设置字体和大小

    text_bbox = draw.textbbox((0, 0), date_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = pil_image.width - text_width -pil_image.width/120
    y = pil_image.height - text_height -pil_image.width/125

    draw.text((x, y), date_text, font=font, fill=(255, 108, 50))  # 红色

    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    output_path = os.path.join(output_path, os.path.basename(image_path))
    cv2.imwrite(output_path, image)

def check_json():
    file_list=os.listdir("./")
    for file in file_list:
        if file.endswith(".json"):
            json_path=os.path.join("./",file)
            break
        else:
            json_path=None
    try:
        with open(json_path,"r") as f:
            data=json.load(f)
        data_path=data["data_path"]
        output_path=data["output_path"]
        mode=data["mode"]
        check_path(output_path)
    except:
        """
        no json setting
        """
        data_path=input("Please input the path of the data folder:")
        print("\n")
        output_path=input("Please input the path of the output folder:")
        print("\n")
        mode=int(input("Please input the mode:"))
        print("\n")
        check_path(output_path)
    return data_path,output_path,mode

def mode0(date,image_path,output_path):
    now_date=date[0]
    year=(now_date.split(":")[0])
    month=now_date.split(":")[1]
    day=now_date.split(":")[2]
    date_text=f"{year}:{month}:{day}"
    font_path='./font/SuTunShiZhongTi-Bold.ttf'
    image = cv2.imread(image_path)
    if image is None:
        status_code=1
        check_condition(status_code)
        pass
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)

    draw = ImageDraw.Draw(pil_image)
    font = ImageFont.truetype(font_path, pil_image.width/25)  # 设置字体和大小

    text_bbox = draw.textbbox((0, 0), date_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = pil_image.width - text_width -pil_image.width/120
    y = pil_image.height - text_height -pil_image.width/125

    draw.text((x, y), date_text, font=font, fill=(255, 108, 50))  # 红色

    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    
    output_path = os.path.join(output_path, os.path.basename(image_path))
    cv2.imwrite(output_path, image)