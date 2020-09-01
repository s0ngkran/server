import paramiko
import matplotlib.pyplot as plt
import numpy as np
import datetime
host = ###
port = ###
username = ###
password = ###

command = "cd skd/batchnorm/train02; cat tr32_seed10"
command = input('command => ')
print('''
\nshow_position
1 2 3
4 5 6
''')
show_pos = input('show_position => ')
x = int(show_pos)-1 if int(show_pos)<4 else int(show_pos)-4
x *= 500
y = 0 if int(show_pos) < 4 else 1
y *= 500

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

def readfile(dat):
    loss = []
    validation = []
    testing = []
    for i in range(len(dat)):
        if dat[i][:6] == 'epoch=':
            try:
                loss_ = dat[i].split('loss=')[1][:-1]
                ep = dat[i].split('loss=')[0].split()[1]
                loss_ = float(loss_)
                ep = int(ep)
                loss.append([ep,loss_])
            except: pass
            try:
                a = dat[i].split()
                ep = a[0].split('epoch=')[1]
                loss_ = a[1].split('loss=')[1]
                loss_ = float(loss_)
                ep = int(ep)
                loss.append([ep,loss_])
            except: pass
            try:
                loss_ = dat[i].split('loss_va=')[1][:-1]
                ep = dat[i].split('loss_va=')[0].split()[1]
                loss_ = float(loss_)
                ep = int(ep)
                validation.append([ep,loss_])
            except: pass
            try:
                a = dat[i].split()
                ep = a[0].split('epoch=')[1]
                loss_ = a[1].split('loss_va=')[1]
                loss_ = float(loss_)
                ep = int(ep)
                validation.append([ep,loss_])
            except: pass
            try:
                loss_ = dat[i].split('te_acc=')[1][:-1]
                ep = dat[i].split('te_acc=')[0].split()[1]
                loss_ = float(loss_)
                ep = int(ep)
                testing.append([ep,loss_])
            except: pass
            try:
                a = dat[i].split()
                ep = a[0].split('epoch=')[1]
                loss_ = a[1].split('te_acc=')[1]
                loss_ = float(loss_)
                ep = int(ep)
                testing.append([ep,loss_])
            except: pass
    print('ploting')
    lo = np.array(loss)
    plt.plot(lo[:,0],lo[:,1],'r.',label='training loss')
    va = np.array(validation)
    plt.plot(va[:,0],va[:,1],'b.-',label='validation loss')
    te = np.array(testing)
    plt.plot(te[:,0],te[:,1]/10000,'g.-',label='testing accuracy')
    plt.legend()
    plt.xlabel('epoch')
    plt.ylabel('loss')
    #plt.ylim((0,4))
    plt.grid()      

while True:
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    readfile(lines)
    plt.title(command.split('cat ')[1] +'\n'+ str(datetime.datetime.now()))
    mngr = plt.get_current_fig_manager()
    # to put it into the upper left corner for example:
    mngr.window.setGeometry(x,y+30,500, 500)
    plt.pause(1)
    plt.cla()
    
