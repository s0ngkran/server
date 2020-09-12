import torch 
import torch.optim as optim
import time as t
import os
from torch2img import torch2img


from hand_model_c3_dropout import hand_model
indexPredL, indexPredS = 2, 3
from test_function_old import Tester


class Tester_img:
    def __init__(self, weight, img_folder, pkl_folder, gts_folder, gtl_folder, savename, savefolder
                    , indexPredL=indexPredL, indexPredS=indexPredS, suffix_gt=''):
        assert img_folder[-1] == gts_folder[-1] == gtl_folder[-1] == savefolder[-1] == '/'
        print('init tester')
        self.indL, self.indS = indexPredL, indexPredS
        self.savename = savename
        self.savefolder = savefolder
        

        try:
            checkpoint = torch.load(weight)
            cuda = True
        except :
            checkpoint = torch.load(weight, map_location={'cuda:0': 'cpu'})
            cuda = False

        if cuda:
            self.model = hand_model().cuda()
        else:
            self.model = hand_model()
        self.optimizer = optim.Adam(self.model.parameters())
        self.cuda = cuda
        print('cuda=',self.cuda)

        self.model.load_state_dict(checkpoint['model_state_dict'])           #
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])   #
        self.epoch = checkpoint['epoch']                                     #
        self.times = [checkpoint['time']]                                    #
        print('loaded model\'s stage')

        self.img_folder = img_folder
        for _,__,img_names in os.walk(img_folder):
            print('fin walk')
        self.img_names = [self.img_folder+img_name for img_name in img_names]
        assert int(img_names[0][:10]) > 0 
        namei = [img_name[:10] for img_name in img_names]
        self.namei = namei
        self.gts_names = [gts_folder+name+suffix_gt for name in namei]
        self.gtl_names = [gtl_folder+name+suffix_gt for name in namei]

        self.genimg = torch2img(savename) # init torch2img class
        self.tester = Tester(pkl_folder)
    def feed(self, img):
        self.model.eval()
        with torch.no_grad():
            out = self.model(img)
        return out[self.indL], out[self.indS]
    def test(self):
        lst = zip(self.img_names, self.gts_names, self.gtl_names, self.namei)
        for i, (img_name, gts_name, gtl_name, namei) in enumerate(lst):
            if self.cuda:
                img = torch.load(img_name).unsqueeze(0).cuda()
                gts = torch.load(gts_name).unsqueeze(0).cuda()
                gtl = torch.load(gtl_name).unsqueeze(0).cuda()
            else:
                img = torch.load(img_name).unsqueeze(0)
                gts = torch.load(gts_name).unsqueeze(0)
                gtl = torch.load(gtl_name).unsqueeze(0)
            filename = str(int(namei)).zfill(3)
           
            header_msg = 'ep' + str(self.epoch) + '_' + str(int(namei))
            out = self.feed(img)
            self.genimg.genimg_(img, out, gts, gtl, filename, msg = header_msg, savefolder=self.savefolder)

            index = [int(namei)]
            self.tester.addtable(out, index)
            print(namei, i+1,'/', len(self.img_names))
        auc = self.tester.getacc(self.savefolder+'accfile')
        return auc
        
if __name__ == "__main__":
    print('start')
    import time
    train_n = input('train>>>')
    epoch = (input('epoch>>>'))
    seed = (input('seed>>>'))
    t0 = time.time()
    weight = 'save/train%s_epoch%s_seed%s.pth'%(train_n.zfill(2),epoch.zfill(10),seed)
    img_folder = '../data014/testing/img_torch_c3/'
    pkl_file = '../data014/testing/pkl/'
    gts_folder = '../data014/testing/gts/'
    gtl_folder = '../data014/testing/gtl/'
    savename = 'test_tr11'
    savefolder = 'test_each/'
    
    tester = Tester_img(weight, img_folder, pkl_file, gts_folder, gtl_folder, savename,  savefolder)
    auc = tester.test()
    print('auc = ', auc)
    print('finish')
    t = time.time-t0
    print('time', t/60, 'mins')
