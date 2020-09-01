import torch 
from torchvision.utils import save_image
import numpy as np
import cv2
# import matplotlib.pyplot as plt
import torch.nn.functional as F
def write(torch_img, inverse = True, filename = 'temp'):
    assert len(torch_img.shape) in [2,3]
    filename = filename + '.jpg'
    if len(torch_img.shape) == 3:
        channel = torch_img.shape[0]
        assert channel in [3,20,11,2], '[channel, x, y] need channel in [3, 20, 11] but get ' + str(torch_img.shape)
        if channel == 20:
            #gtl mode
            torch_img = torch_img.mean(0)
            mx = torch_img.max()
            mn = torch_img.min()
            torch_img = (torch_img-mn)/(mx-mn)
            mx = torch_img.max()
            mn = torch_img.min()
            mean = torch_img.mean()
            mid = (mx-mn)/2
            if mean<mid:
                inverse = True
            else: inverse = False
        elif channel == 11:
            torch_img = torch_img.max(0)[0]
        elif channel == 2:
            torch_img = torch_img.max(0)[0]
    if len(torch_img.shape) == 2:
        img = torch_img.transpose(1,0) # get horizontal
    if len(torch_img.shape) == 3:
        inverse = False
        img = torch_img[(2,1,0),:,:].transpose(1,2) # get horizontal
    if inverse:
        img = 1-img
    save_image(img, filename)
def write_(torch_img, inverse = True, filename = 'temp'):
    assert len(torch_img.shape) in [2,3]
    filename = filename + '.jpg'
    if len(torch_img.shape) == 3:
        channel = torch_img.shape[0]
        assert channel in [3,20,11,2], '[channel, x, y] need channel in [3, 20, 11] but get ' + str(torch_img.shape)
        if channel == 20:
            #gtl mode
            torch_img = torch_img.mean(0)
            mx = torch_img.max()
            mn = torch_img.min()
            torch_img = (torch_img-mn)/(mx-mn)
            mx = torch_img.max()
            mn = torch_img.min()
            mean = torch_img.mean()
            mid = (mx-mn)/2
            if mean<mid:
                inverse = True
            else: inverse = False
        elif channel == 11:
            torch_img = torch_img.max(0)[0]
        elif channel == 2:
            torch_img = torch_img.mean(0)
    if len(torch_img.shape) == 2:
        img = torch_img.transpose(1,0) # get horizontal
    if len(torch_img.shape) == 3:
        inverse = False
        img = torch_img[(2,1,0),:,:].transpose(1,2) # get horizontal
    if inverse:
        img = 1-img
    save_image(img, filename)
def vcat(tensors):
    n = len(tensors)
    for i in range(n):
        write(tensors[i], filename='temp%s'%i)
    npys = [cv2.imread('temp%s.jpg'%i) for i in range(n)]
    cv2.imwrite('temp.jpg',cv2.vconcat(npys))
def vcat_(tensors):
    n = len(tensors)
    for i in range(n):
        write_(tensors[i], filename='temp%s'%i)
    npys = [cv2.imread('temp%s.jpg'%i) for i in range(n)]
    cv2.imwrite('temp.jpg',cv2.vconcat(npys))  

def test_write():
    # t = torch.rand([3,60,60])
    # t = torch.rand([60,60])
    t = torch.load('ex_gtl')
    write(t)
    read()
def test_vcat():
    t = torch.load('ex_img')
    ts = torch.stack([t,t,t])
    vcat(ts)
    read()
def test_hcat():
    t = torch.rand([3,3,60,60])
    t = torch.load('ex_img')
    ts = [t,t,t]
    img = hcat(ts)
    cv2.imwrite('temp.jpg',img)
    read()
def read():
    import matplotlib.pyplot as plt
    img = cv2.imread('temp.jpg')
    plt.imshow(img)
    # plt.colorbar()
    plt.show()
def test_cat():
    import torch 
    # t1 = torch.rand([60,60])
    t1 = torch.load('ex_img')[0]
    tt = [t1,t1,t1]
    img = cat_x(tt)
    write(img, inverse=True)
    read()
def resize(torch, size):
    assert len(torch.shape) == len(size) == 2
    import torch.nn.functional as F
    resized = F.interpolate(torch.unsqueeze(0).unsqueeze(0), size, mode='bicubic')
    return resized.squeeze().squeeze()
def test_resize():
    img = torch.load('0000000004')[0]
    print('img=',img.shape)
    gts = torch.load('0000000004_')
    gts = torch.max(gts, dim=0)[0]
    print('gts=',gts.shape)
    gts = resize(gts, [40,40])
    print('gts_resized=',gts.shape)

    # img = img*0.5+gts*0.5
    write(gts)
    read()
def test_write_gtl():
    img = torch.load('0000000004_')
    img = torch.mean(img, dim=0)
    img = resize(img, [480,480])
    write(img, inverse=True)
    read()
def write_all(tensors):
    imgs = []
    for i,tensor in enumerate(tensors):
        if i!=5:
            vcat(tensor)
        else:
            vcat_(tensor)
        imgs.append(cv2.imread('temp.jpg'))
    img = cv2.hconcat(imgs)
    # cv2.imwrite('temp.jpg',img)
    return img
def test_write_all():
    t = torch.load('ex_img')
    ts = torch.stack([t, t, t])
    tss = [ts,ts,ts]
    write_all(tss)
    cv2.imwrite('temp.jpg',img)
    read()

def feed():
    from hand_model import hand_model
    import torch
    import torch.nn.functional as F
    # model = hand_model()
    img = torch.load('ex_img')
    img = torch.stack([img,img])
    # out = model(img)

    gts = torch.load('ex_gts')
    gtl = torch.load('ex_gtl')
    gts = torch.stack([gts, gts])
    gtl = torch.stack([gtl, gtl])

   
    # gts_pred = out[11]
    # gtl_pred = out[5]
    
    print(img.shape, gts.shape)
    # print(img[:,0,:,:].shape, gts.max(0)[0].shape)
    img = F.interpolate(img, [60,60])
    img_ = img[:,0,:,:]*0.4 + gts.max(1)[0]*0.6
    # print(img.shape, gts.shape, gtl.shape, gts_pred.shape, gtl_pred.shape)
    write_all([img,img_,gts,gtl])
    # write_all([img, gts, gts_pred, gtl, gtl_pred])
    read()
def genimg(img, out, gts, gtl):
    img = F.interpolate(img, [60,60])
    gts_pred = out[11]
    gtl_pred = out[5]
    img_ = img[:,0,:,:]*0.4 + gts_pred.max(1)[0]*0.6
    write_all([img,img_,gts,gts_pred,gtl,gtl_pred])
def genimg_(img, out, gts, gtl, filename, msg='temp'): #img = [batch, ch, x, y]
    img = F.interpolate(img, [45,45])
    gts_pred = out[1]
    gtl_pred = out[0]
    img_ = img[:,0,:,:]*0.4 + gts_pred.max(1)[0]*0.6
    img = torch.cat([img, img, img], dim=1)
    img = write_all([img,img_,gts,gts_pred,gtl,gtl_pred])
    img = write_header_msg(img, msg)
    cv2.imwrite('temp.jpg',img) # for send to line
    cv2.imwrite('saveimg/'+filename+'.jpg', img)
def write_header_msg(oriimg, msg):
    assert len(oriimg.shape) == 3
    assert type(msg)==str, 'msg argument needs str type'
    img = np.zeros((35, oriimg.shape[1], 3))
    font = cv2.FONT_HERSHEY_SIMPLEX 
    org = (10, 22) 
    fontScale = 0.6
    color = (255, 255, 255)
    thickness = 2
    img = cv2.putText(img, msg, org, font,  
                    fontScale, color, thickness, cv2.LINE_AA) 
    print(img.shape , oriimg.shape)
    img = np.vstack((img, oriimg))
    print(img.shape)
    cv2.imwrite('testhead.jpg', img)
    return img
    # cv2.imwrite('header.jpg',img)
def test_write_header_msg():
    tempimg = cv2.imread('temp.jpg')
    write_header_msg(tempimg, 'tr te va epoch')
if __name__ == '__main__':
    # test_write_all()
    # test_resize()
    # feed()
    # test_vcat() 
    # test_write()   
    # a = torch.rand(torch.Size([5, 1, 45, 45]))
    # img = torch.cat([a, a, a], dim=1)
    # print(img.shape)
    test_write_header_msg()
