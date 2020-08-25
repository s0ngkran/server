# img_aug.py
* aug all image in a folder

## resize and crop
* resize to specific size
* no problem with portrait or landscape image
* crop from center
```python
import img_aug
img_ = img_aug.resizeAndCrop(folder, savefolder, 360)
```
![alt text](https://github.com/s0ngkran/server/blob/master/image_augment/ex_img_augment.png)

## replace background
* aug all image in a folder
