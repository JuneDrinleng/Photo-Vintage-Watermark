from model import *
from tqdm import tqdm

if __name__=="__main__":
    data_path,output_path,mode=check_json()
    if os.path.isdir(data_path)==True:
        image_list=os.listdir(data_path)
        for image in tqdm(image_list):
            image_path=os.path.join(data_path,image)
            date=get_image_date(image_path)
            if mode==0:
                mode0(date=date,image_path=image_path,output_path=output_path)
    else:
        if data_path.endswith(".jpg") or data_path.endswith(".jpeg") or data_path.endswith(".png"):
            date=get_image_date(data_path)
            if mode==0:
                mode0(date=date,image_path=data_path,output_path=output_path)
        else:
            status_code=4
            check_condition(status_code)
