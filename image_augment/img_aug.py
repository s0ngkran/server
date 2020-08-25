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
if __name__ == "__main__":
    folder = 'green_screen/raw/'
    savefolder = 'green_screen/img/'
    resizeto = 360
    resizeAndCrop(folder, savefolder, resizeto)


