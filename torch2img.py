import torch 
import cv2
import numpy as np
def write(torch):
    assert len(torch.shape) == 2
    img = np.array(torch*255)
    cv2.imwrite('temp.jpg', img)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    t = torch.rand([60,60])
    write(t)
    img = cv2.imread('temp.jpg')
    plt.imshow(img)
    plt.show()
