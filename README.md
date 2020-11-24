# monitor2.py
* auto monitor the log file
* set realtime mode by change the value in monitor.txt to 'realtime'
```cmd
>python monitor2.py
```
![alt text](https://github.com/s0ngkran/server/blob/master/example/ex_monitor2.jpg)
</br></br></br>

# line.py
* send massage
* send torch image
* wait 10 sec if connection error is raised.
```python
import line
line = Line(os.path.basename(__file__))
line.send('hi')
```
```python
import torch
t = torch.rand([100,100])
line.send_torch(t)
```
![alt text](https://github.com/s0ngkran/server/blob/master/example/ex_send_line.jpg)
</br></br></br>

# img_aug.py
* aug all image in a folder
```python
import img_aug
```

## resize and crop
* resize to specific size
* no problem with portrait or landscape image
* crop from center
* ready to go to hand_keypoint_generator program
```python
img_aug.resizeAndCrop(folder, savefolder, 360)
```
![alt text](https://github.com/s0ngkran/server/blob/master/image_augment/ex_img_augment.png)

## rotate
* rotate image and groundtruth in one command
```python
angle = 30
img_folder = 'random_background/training_mix/'
gt_file = 'gt_training.torch'
save_imfolder = 'random_background/training_aug/'
save_pklfolder = 'random_background/training_aug_pkl/'
start_name = 2792
img_aug.aug_rotate(angle, img_folder, gt_file, save_imfolder, save_pklfolder, start_name, suffix=None)
```
![alt text](https://github.com/s0ngkran/server/blob/master/image_augment/ex_rotate.jpg)

## scale
* rescale image and groundtruth in one command
```python
scale = 0.7
img_folder = 'example_folder/'
gt_file = 'gt_training.torch'
save_imfolder = 'example_folder_save/'
save_pklfolder = save_imfolder
start_name = 352
aug_scale(scale, img_folder, gt_file, save_imfolder, save_pklfolder, start_name, suffix=None)
```
![alt text](https://github.com/s0ngkran/server/blob/master/image_augment/ex_scale.jpg)

## replace background
* replace images with random background
```python
img_aug.replace_bg(folder_img, folder_bg, savefolder)
```
![alt text](https://github.com/s0ngkran/server/blob/master/image_augment/ex_replace.png)

## pkl files to torch
* the folder with other files are allowed
```python
comment = '360x360 => 2 point'
img_aug.pkl2torch(pkl_folder, savefile, comment, suffix='_2p.pkl')
```
![alt text](https://github.com/s0ngkran/server/blob/master/image_augment/ex_pkl2torch.jpg)

## rename
* the folder with other files are allowed
```python
folder = 'random_background/new/'
last_num = 10
start_at = 6
img_aug.rename_in_folder(folder, last_num, start_at, '.bmp')
```
![alt text](https://github.com/s0ngkran/server/blob/master/image_augment/ex_rename.jpg)

## rename when delete a file
* the folder with other files are allowed
```python
folder = 'test_folder/'
img_aug.rename_all(folder)
```
![alt text](https://github.com/s0ngkran/server/blob/master/image_augment/ex_rename_all.png)

