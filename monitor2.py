import paramiko
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
from ck_loss import getfromline


def readfile(data):
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
        plt.plot(testing1[:,0],testing1[:,1]*400,'m.-',label='testing1 acc*400')
        plt.plot(testing2[:,0],testing2[:,1]*400,'g.-',label='testing2 acc*400')

    plt.legend()
    plt.xlabel('epoch')
    plt.ylabel('loss')
    #plt.ylim((0,4))
    plt.grid()   

def run(command, show_pos):
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
    print('show_pos=',show_pos)
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
            readfile(lines)
            plt.title(command.split('cat ')[1] +'\n'+ str(datetime.datetime.now()))
            mngr = plt.get_current_fig_manager()
            # to put it into the upper left corner for example:
            mngr.window.setGeometry(x,y+30,500, 500)
            
            if fail_state == 1:
                fail_state = 0
                print('success...')

            with open('monitor.txt','r') as f:
                realtime = f.readline()
            if realtime == 'realtime':
                print('realtime mode '+command.split('cat ')[1])
                plt.pause(120)
            else:
                plt.show()
            
            plt.cla()

        except :
            print(lines, 'try again in 10sec...')
            fail_state = 1
            time.sleep(10)

            
if __name__ == "__main__":

    command = "cd skd/train0027; cat tr01.txt"
    show_pos = 1
    run(command, show_pos)
    
