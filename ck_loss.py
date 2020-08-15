import matplotlib.pyplot as plt
import numpy as np
def getfromline(line, text):
    line = line.split(' ')
    for dat in line:
        if text in dat:
            _ans = dat.split(text)[1]
            ans = _ans if dat[-1] != '\n' else _ans[:-1]
            try: ans = float(ans)
            except: pass
            return ans
if __name__ == '__main__':
        
    print('start program')

    print('reading')
    filename = 32
    name = 'tr'+str(filename).zfill(2) +'_seed1'
    name = '_tr01_seed1.txt'
    with open(name,'r') as f:
        dat = f.readlines()
    print('loss appending')
    loss = []
    validation = []
    testing = []
    for line in dat:
        try:
            epoch = getfromline(line, 'epoch=')
            loss_ = getfromline(line, 'loss=')
            va_loss_ = getfromline(line, 'loss_va=')
            if loss_ != None: loss.append([epoch, loss_])
            if va_loss_ != None: validation.append([epoch, va_loss_])
        except :pass


    print('ploting')
    lo = np.array(loss)
    va = np.array(validation)
    # te = np.array(testing)
    plt.plot(lo[:,0],lo[:,1],'r.-',label='training loss')
    plt.plot(va[:,0],va[:,1],'b.-',label='validation loss')
    # plt.plot(te[:,0],te[:,1]/10000,'g.-',label='testing accuracy')

    plt.legend()
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.ylim((0,500000000*0.1))
    plt.grid()
    plt.show()




    