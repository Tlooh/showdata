"""
* 获取目录下的所有图像
 1.获取所有图像后缀的文件

* 获取目录下的所有子目录
 2. 不同子目录作为对比
"""
import os
from typing import List
from PIL import Image

IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp']

def _load_and_resize_image(image, resize=None):
    image = Image.open(image).convert('RGB')
    if resize:
        image = image.resize(resize)
        # print(image.size)
    return image

def is_image(filename):
    return filename.split('.')[-1].lower() in IMAGE_EXTENSIONS

# 按名称排序 
def split_images_and_dir(directory, sort=True):
    image_paths = []
    dir_paths = []
    for f in os.listdir(directory):
        if is_image(f):
            f_path = os.path.join(directory, f)
            image_paths.append(f_path)
        elif os.path.isdir(os.path.join(directory, f)):
            dir_paths.append(os.path.join(directory, f))

    if sort:
        image_paths.sort()
        dir_paths.sort()
    return image_paths, dir_paths


def get_images(directory:str, only_imgs: bool = False, sort:bool = True, ) -> List[List[str]]:
    all_class_images = []

    images_paths, dir_paths = split_images_and_dir(directory, sort)
    if only_imgs:
        images = images_paths
        all_class_images.append(images)
    
    elif not only_imgs:
        for dir_path in dir_paths:
            sub_dir_images_paths, _ = split_images_and_dir(dir_path, sort)
            all_class_images.append(sub_dir_images_paths)
    # TODO：Test
    # else:
    #     for root, dirs, files in os.walk(directory):
    #         images,_ = split_images_and_dir(root, sort)
    #         print(images)
    #         all_class_images.append(images)
    
    return all_class_images
    

def concat_images_with_spacing(all_class_images, spacing=20):
    if isinstance(spacing, list) or isinstance(spacing, tuple):
        row_spacing, col_spacing = spacing
    else:
        row_spacing, col_spacing = spacing, spacing
    cls_nums = len(all_class_images)
    pil_all_class_images = [[_load_and_resize_image(img, (512,512)) for img in row] for row in all_class_images]

    # Get the maximum height and width of each column
    max_H, max_W = 0, 0
    print([len(cls) for cls in pil_all_class_images])
    max_nums_of_images = max([len(cls) for cls in pil_all_class_images])
    for images_row in pil_all_class_images:
        for image in images_row:
            max_H = max(max_H, image.height)
            max_W = max(max_W, image.width)

    total_height = max_H * max_nums_of_images + row_spacing * (max_nums_of_images - 1)
    total_width = max_W * cls_nums + col_spacing * (cls_nums - 1)
    
    # Create a new image with the maximum height and width
    new_image = Image.new('RGB', (total_width, total_height), (255, 255, 255))

    # Paste each image into the new image
    x_offset = 0
    for cls_idx, images_row in enumerate(pil_all_class_images):
        y_offset = 0
        cur_cls_nums = len(images_row)

        for i, image in enumerate(images_row):
            new_image.paste(image, (x_offset, y_offset))
            if i < cur_cls_nums - 1:
                y_offset += max_H + row_spacing
            else:
                y_offset += max_H
        if cls_idx < cls_nums - 1:
            x_offset += max_W + col_spacing
        else:
            x_offset += max_W
    
    return new_image
    

def example():
    directory = 'showdata/assets/test'
    all_class_images = get_images(directory, only_imgs=True) # [[1.png,2.png,……], [1.png,2.png,……], [1.png,2.png,……]]
    save_img = concat_images_with_spacing(all_class_images)
    save_img.save('showdata/assets/concat.jpg')
    print(all_class_images)

if __name__ == "__main__":
    example()

