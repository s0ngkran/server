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
def ex_replace_bg():
    folder_img = 'green_replaced/'
    folder_bg = 'bg_imgs/img/'
    savefolder = 'replaced_background/'
    replace_bg(folder_img, folder_bg, savefolder)
def img2torch(folder_img, savefolder):
    import torch 
    assert folder_img[-1] == savefolder[-1] == '/'
    for _,__,img_names in os.walk(folder_img):
        print('fin walk')
    for i, img_name in enumerate(img_names):
        name = img_name[6:16]
        assert int(name)
        img = cv2.imread(folder_img + img_name) # y,x,ch
        img = torch.FloatTensor(img/255).transpose(0,2) # ch,x,y
        torch.save(img, savefolder + name)
        print(img_name, i+1, len(img_names))
def img2torch_gray(folder_img, savefolder):
    import torch 
    assert folder_img[-1] == savefolder[-1] == '/'
    for _,__,img_names in os.walk(folder_img):
        print('fin walk')
    for i, img_name in enumerate(img_names):
        name = img_name[6:16]
        assert int(name)
        img = cv2.imread(folder_img + img_name) # y,x,ch
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # y,x
        img = torch.FloatTensor(img/255).transpose(0,1).unsqueeze(0) # ch=1,x,y
        torch.save(img, savefolder + name)
        print(img_name, i+1, len(img_names))
def pkl2torch(pkl_folder, savefile, comment, suffix='_2p.pkl'):
    import torch 
    import pickle
    #test
    try:
        testload = pkl_folder + str(1).zfill(10) + suffix
        with open(testload, 'rb') as f:
            data = pickle.load(f)
            keypoint = data['keypoint']
            covered_point = data['covered_point']
        fail = False
    except:
        fail = True

    assert fail == False, 'fail to load %s'%testload

    i = 0
    keys = []
    covs = []
    while i!=-1:
        try:
            key, cov = [], []
            name = str(i).zfill(10) + suffix
            if i==0: name = str(1).zfill(10) + suffix
            with open(pkl_folder+name, 'rb') as f:
                data = pickle.load(f)
                keypoint = data['keypoint']
                covered_point = data['covered_point']
            for ind in range(len(keypoint)):
                key.append(keypoint[ind])
                cov.append(covered_point[ind])
            key = torch.IntTensor(key)
            cov = torch.IntTensor(cov)
            keys.append(key)
            covs.append(cov)
            print(name)
            i+=1
        except:
            keys = torch.stack(keys)
            covs = torch.stack(covs)
            torch.save({'keypoint':keys
                        ,'covered_point':covs
                        ,'comment':comment
            }, savefile)
            print('saved', savefile)
            i = -1
def rename_in_folder(folder, last_num, start_at, suffix):
    assert folder[-1] == '/'
    assert type(last_num) == type(start_at) == int
    assert type(suffix) == str
    try:
        for i in range(last_num):
            i = last_num-i
            name = str(i).zfill(10)
            src = folder + name + suffix
            

            i += start_at - 1
            name = str(i).zfill(10)
            dst = folder + name + suffix
         
            os.rename(src, dst)
            print(src, '>>>', dst)
        
        #del
        for i in range(start_at-1):
            i += 1
            name = str(i).zfill(10) + suffix
            os.remove(folder + name)
    except:
        print('fin')
if __name__ == "__main__":
    # resizeAndCrop('random_background/raw/training_extend/', 'random_background/training_extend/', 360)
    # ['green_screen/','replaced_background/','replaced_green/','random_background/']
    # for i in ['replaced_background/','replaced_green/']:
    #     folder_img = 'training/img/' + i
    #     savefolder = 'training/img_torch/3channel/' + i
    #     img2torch(folder_img, savefolder)

    # pkl_folder = 'random_background/validation/'
    # savefile = 'gt_validation.torch'
    # pkl2torch(pkl_folder, savefile, '360x360 => 2 point', suffix='_2p.pkl')

    folder = 'random_background/new/'
    last_num = 10
    start_at = 6
    rename_in_folder(folder, last_num, start_at, '.bmp')



