import cv2
import os 

def resizeAndCrop(folder, savefolder, resizeto):
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
        else:
            re_y = resizeto
            re_x = resizeto*x/y
        dim = (int(re_x), int(re_y))
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        resized = resized[:resizeto, :resizeto]
        cv2.imwrite(savefolder+namei+'.jpg', resized)
        print(namei)
        i+=1
    print('finish resize and crop')
if __name__ == "__main__":
    folder = 'training/'
    savefolder = 'temp/'
    resizeto = 360
    resizeAndCrop(folder, savefolder, resizeto)


