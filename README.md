# img_aug.py
* aug all image in a folder
```python
import img_aug
```

## resize and crop
* resize to specific size
* no problem with portrait or landscape image
* crop from center
```python
img_aug.resizeAndCrop(folder, savefolder, 360)
```
![alt text](https://github.com/s0ngkran/server/blob/master/image_augment/ex_img_augment.png)

## replace background
* replace images with random background
```python
replace_bg(folder_img, folder_bg, savefolder)
```
![alt text](https://github.com/s0ngkran/server/blob/master/image_augment/ex_replace.png)
