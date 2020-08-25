import cv2
import os 

def resizeAndCrop(folder, savefolder, resizeto, filename = '.bmp'):
    for _,__,fname in os.walk(folder):
        print('fin walk')
    i = 1
    for name in fname:
        namei = str(i).zfill(10)
        img = cv2.imread(folder+name)
        y, x, channel = img.shape
        #x/y = rex/rey
        if x < y :
            re_x = resizeto
            re_y = resizeto*y/x
            crop_x1 = 0
            crop_x2 = resizeto
            cen = re_y/2
            crop_y1 = cen-resizeto/2
            crop_y2 = crop_y1 + resizeto
        else:
            re_y = resizeto
            re_x = resizeto*x/y
            crop_y1 = 0
            crop_y2 = resizeto
            cen = re_x/2
            crop_x1 = cen-resizeto/2
            crop_x2 = crop_x1 + resizeto 
        re_x, re_y, crop_x1, crop_x2, crop_y1, crop_y2 = [int(i) for i in list((re_x, re_y, crop_x1, crop_x2, crop_y1, crop_y2))]
        dim = (re_x, re_y)
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

        croped = resized[crop_y1:crop_y2, crop_x1:crop_x2]
        cv2.imwrite(savefolder+namei+filename, croped)
        print(namei)
        i+=1
    print('finish resize and crop')
def ex_resizeAndCrop():
    folder = 'bg_imgs/raw/'
    savefolder = 'bg_imgs/img/'
    resizeto = 360
    resizeAndCrop(folder, savefolder, resizeto)
def replace_bg(folder_img, folder_bg, savefolder, filename='.bmp'):
    import random
    for _,__,img_names in os.walk(folder_img):
        print('fin walk imgs')
    for _,__,bg_names in os.walk(folder_bg):
        print('fin walk backgrounds')
    
    # test
    img = cv2.imread(folder_img + img_names[0])
    bg_name = random.choice(bg_names)
    bg = cv2.imread(folder_bg + bg_name)
    assert img.shape == bg.shape 

    for i, img_name in enumerate(img_names):
        img = cv2.imread(folder_img + img_name)
        bg_name = random.choice(bg_names)
        bg = cv2.imread(folder_bg + bg_name)

        # get mask
        c1 = img[:,:,0]==0
        c2 = img[:,:,1]==255
        c3 = img[:,:,2]==0
        mask = c1*c2*c3
        mask.reshape([img.shape[0],img.shape[1]])
        img[mask] = bg[mask]

        cv2.imwrite(savefolder + img_name, img)
        print(img_name, i+1,'/', len(img_names))
    print('fin all')
    
if __name__ == "__main__":
    folder_img = 'green_replaced/'
    folder_bg = 'bg_imgs/img/'
    savefolder = 'replaced_background/'
    replace_bg(folder_img, folder_bg, savefolder)


