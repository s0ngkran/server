# monitor2.py
* auto monitor the log file
* set realtime by change the value in monitor.txt to 'realtime'
```python
if __name__ == "__main__":
    command = "cd skd/train0027; cat tr01.txt"
    run(command)
```
![alt text](https://github.com/s0ngkran/server/blob/master/example/ex_monitor.png)
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

## pkl files to torch
* the folder with other file allowed
```python
comment = '360x360 => 2 point'
pkl2torch(pkl_folder, savefile, comment, suffix='_2p.pkl')
```
![alt text](https://github.com/s0ngkran/server/blob/master/image_augment/ex_pkl2torch.jpg)

## rename
```python
folder = 'random_background/new/'
last_num = 10
start_at = 6
rename_in_folder(folder, last_num, start_at, '.bmp')
```
![alt text](https://github.com/s0ngkran/server/blob/master/image_augment/ex_rename.jpg)
