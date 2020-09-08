import paramiko
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
from ck_loss import getfromline

def readfile(data, lim=''):
    if lim == '': lim = None
    training = []
    validation = []
    testing1 = []
    testing2 = []
    for line in data:
        try:
            epoch = getfromline(line, 'epoch=')
            tr_loss = getfromline(line, 'loss=')
            va_loss = getfromline(line, 'loss_va=')
            te_loss = getfromline(line, 'loss_te=')

            if tr_loss != None: training.append([epoch, tr_loss])
            if va_loss != None: validation.append([epoch, va_loss])
            if te_loss != None:
                list_ = line.split('loss_te=')[1]
                if list_[-1] == '\n': list_ = list_[:-1]
                assert list_[0] == '[', 'check loss_te format'
                # split [ , ] format
                te_loss = list_.split('[')[1].split(']')[0].split(',')
                te_loss = [float(i) for i in te_loss]
                testing1.append([epoch, te_loss[0]])
                testing2.append([epoch, te_loss[1]])
        except :pass
    training = np.array(training)
    validation = np.array(validation)
    plt.plot(training[:,0],training[:,1],'r.',label='training loss')
    plt.plot(validation[:,0],validation[:,1],'b.-',label='validation loss')
    if testing1 != []:
        testing1 = np.array(testing1)
        testing2 = np.array(testing2)
        plt.plot(testing1[:,0],testing1[:,1]*100,'m.-',label='testing1 acc*100')
        plt.plot(testing2[:,0],testing2[:,1]*100,'g.-',label='testing2 acc*100')

    plt.legend()
    plt.xlabel('epoch')
    plt.ylabel('loss')
    if lim != None:
        plt.ylim((0,lim))
      
    return testing1, testing2

def run(command, show_pos=1, lim='', check_test_mode=False, epoch='',tr=None):
    host = "202.28.93.225"
    port = 22
    username = "sk"
    password = "sk"

    # command = "cd skd/batchnorm/train02; cat tr32_seed10"
    # command = "cd skd/train0027; cat tr01.txt"
    # command_ = input('file => ')
    # command = command + command_
    # print('''
    # \nshow_position
    # 1 2 3
    # 4 5 6
    # ''')
    # show_pos = input('show_position => ')
    # print('show_pos=',show_pos)
    x = int(show_pos)-1 if int(show_pos)<4 else int(show_pos)-4
    x *= 500
    y = 0 if int(show_pos) < 4 else 1
    y *= 500

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    fail_state = 0
    while True:
        try:
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            testing1, testing2 = readfile(lines, lim=lim)
            plt.title(command.split('cat ')[1] +'\n'+ str(datetime.datetime.now()))
            mngr = plt.get_current_fig_manager()
            # to put it into the upper left corner for example:
            mngr.window.setGeometry(x,y+30,500, 500)
            
            if fail_state == 1:
                fail_state = 0
                print('success...')

            if check_test_mode:
                print('file:',tr,'epoch', epoch)
                for ep, val1 in testing1:
                    if ep == epoch:
                        print('AP testing1=', val1)
                        break
                for ep, val2 in testing2:
                    if ep == epoch:
                        print('AP testing2=', val2)
                        break
                print('mAP =',(val1+val2)/2)
                break
                
                print('AP testing2=',testing2[50])
            else:
                with open('monitor.txt','r') as f:
                    realtime = f.readline()

                if realtime == 'realtime':
                    print('realtime mode '+command.split('cat ')[1])
                    plt.pause(120)
                else:
                    plt.grid() 
                    plt.show()
                    break
                
                plt.cla()

        except :
            print('\n\ntry again in 10sec...')
            fail_state = 1
            time.sleep(10)

def get_input(oldname):
    epoch = 0
    cmode = False
    show_pos = 1
    print('')
    print('--------------------options--------------------')
    print('<str:log_name>  => get graph')
    print('<enter>         => update graph')
    print('<int:epoch>     => get mAP of ')
    print('                   previous log_name at a epoch')
    print('-----------------------------------------------')
    print('')
    tr = input('command>>')
    if tr == '':
        tr = oldname
    elif 'tr' not in tr:
        epoch = int(tr)
        tr = oldname
        cmode = True
        
    elif ' ' in tr:
        cmode = True
        epoch = tr.split(' ')[1]
        epoch = int(epoch)
        tr = tr.split(' ')[0]
    else:
        print('<enter> => Quick choose position 1')
        print('''
        \nshow_position
        1 2 3
        4 5 6
        ''')
        show_pos = input('show_position => ')
        if show_pos == '':show_pos = 1
    command = "cd skd/train0027; cat %s.txt"%tr
    run(command, show_pos=show_pos, lim=100, check_test_mode=cmode, epoch=epoch, tr=tr)
    return tr
if __name__ == "__main__":
    tr = None
    while True:
        tr = get_input(tr)
        print('')
    print('end')
    
    
