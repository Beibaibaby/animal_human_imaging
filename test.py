import numpy as np
import h5py
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
import csv
hf = h5py.File('201217_01_ica_filtered.hdf5', 'r')
print(hf.keys())
filtered = hf.get('filtered')
print(filtered)
arr=filtered[1]

def preprocess(input):
    n_x = 492
    n_y = 642
    arr = input.transpose()
    arr = np.flip(arr,0)
    arr_left = arr[:,:321]
    return arr_left

tem = preprocess(arr)
print(tem.shape)
tem=tem[1:492,0:318]
print(tem.shape)

def upfinder(m):
    upmost = 1000
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            if m[i][j] != 0:
                if i < upmost:
                    upmost = i
    return upmost

def downfinder(m):
    downmost = 0
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            if m[i][j] != 0:
                if i > downmost:
                    downmost = i
    return downmost

def leftfinder(m):
    upmost = 1000
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            if m[i][j] != 0:
                if j < upmost:
                    upmost = j
    return upmost

def rightfinder(m):
    downmost = 0
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            if m[i][j] != 0:
                if j > downmost:
                    downmost = j
    return downmost



def pre():
    n_x = 492
    n_y = 642

    n_node = n_x * n_y

    length = 9000
    ###arr = np.zeros((length,n_node))
    ###$for i in range(length):
    ###    for j in range(n_x):
    ###        for k in range(n_y):
    ###            arr[i,j*n_y+k]=filtered[i,j,k]

    corr = np.zeros(shape=(n_node, n_node))

    for i in range(n_node):
        ts_1 = []
        for index_i in range(length):
            index_x_i = i % n_x
            index_y_i = int(i / n_x)
            ts_1.append(filtered[index_i, index_x_i, index_y_i])
        for j in range(n_node):
            ts_2 = []
            for index_j in range(length):
                index_x_j = j % n_x
                index_y_j = int(j / n_x)
                ts_2.append(filtered[index_j, index_x_j, index_y_j])
            corr[i, j] = pearsonr(ts_1, ts_2)[0]

    with open('test.npy', 'wb') as f:
        np.save(f, corr)





m=np.load('./pictures/m.npy')



mask=np.load('./arr/mask_o.npy')
def makemask():
    print(mask.shape)
    mask_new = np.zeros([491, 318])
    k_i = 491 / 1070
    k_j = 318 / 650
    for i in range(1070):
        for j in range(650):
            if mask[i, j] != 0:
                i_new = int(k_i * i)
                j_new = int(k_j * j)
                mask_new[i_new, j_new] = 1


def makemaskss():
    mask_ss = np.zeros([491, 318])
    k_i = 460 / 1070
    k_j = 270 / 650
    for i in range(1070):
        for j in range(650):
            if mask[i, j] != 0:
                i_new = int(k_i * i) + 20
                j_new = int(k_j * j) + 40
                mask_ss[i_new, j_new] = 1
    np.save('./arr/mask_ss', mask_ss)
mask_ss = np.load('./arr/mask_ss.npy')

def show():
    plt.imshow()
    plt.colorbar()
    plt.savefig('./pictures/temp.png')

akk = tem + mask_ss*200

with open("new_file.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(akk)



def searchregion(matrix,ini_i,ini_j,low_i,low_j):
    reg = []
    i_index = ini_i
    j_index = ini_j

    while True:
        i_curr = i_index
        j_curr = j_index
        while True:
            if matrix[i_curr, j_curr] > 100:
                break
            else:
                reg.append([i_curr, j_curr])
                i_curr = i_curr
                j_curr = j_curr - 1

        i_curr = i_index
        j_curr = j_index
        while True:
            if matrix[i_curr, j_curr] > 100:
                break
            else:
                reg.append([i_curr, j_curr])
                i_curr = i_curr
                j_curr = j_curr + 1
        i_index=i_index-1
        j_index=ini_j
        if matrix[i_index,j_index]> 100:
            break

    #####scan up
    i_index = low_i
    j_index = low_j

    while True:
        i_curr = i_index
        j_curr = j_index
        while True:
            if matrix[i_curr, j_curr] > 100:
                break
            else:
                reg.append([i_curr, j_curr])
                i_curr = i_curr
                j_curr = j_curr - 1

        i_curr = i_index
        j_curr = j_index
        while True:
            if matrix[i_curr, j_curr] > 100:
                break
            else:
                reg.append([i_curr, j_curr])
                i_curr = i_curr
                j_curr = j_curr + 1
        i_index = i_index + 1
        j_index = low_j
        if matrix[i_index, j_index] > 100:
            break
    new_array = [tuple(row) for row in reg]
    uniques = np.unique(new_array)
    return uniques

def regder(matrix,ir,jr):
    iin=ir
    jjn=jr
    up_i = 0
    up_j = 0
    len = 0

    i_curr=iin
    j_curr=jjn
    len_tem = 0
    while True:
        if matrix[i_curr, j_curr] > 100:
            break
        else:
            len_tem= len_tem + 1
            i_curr = i_curr + 1
    if len_tem > len:
        print('tbd')

def searchregion_1(matrix,ini_i,ini_j):
    reg = []
    i_index = ini_i
    j_index = ini_j

    while True:
        while True:
            i_curr = i_index
            j_curr = j_index
            while True:
                if matrix[i_curr, j_curr] > 100:
                    break
                else:
                    reg.append(matrix[i_curr, j_curr])
                    i_curr = i_curr
                    j_curr = j_curr - 1

            i_curr = i_index
            j_curr = j_index
            while True:
                if matrix[i_curr, j_curr] > 100:
                    break
                else:
                    reg.append(matrix[i_curr, j_curr])
                    i_curr = i_curr
                    j_curr = j_curr + 1
            i_index = i_index - 1
            if matrix[i_index, j_index] > 100:
                break
        if matrix[i_index, j_index + 1]<100:
            j_index = j_index + 1
        elif matrix[i_index, j_index - 1]<100:
            j_index = j_index - 1
        else:
            print(i_index, j_index)
            break

 #########scan down
    i_index = ini_i + 1
    j_index = ini_j

    while True:
        while True:
            i_curr = i_index
            j_curr = j_index
            while True:
                if matrix[i_curr, j_curr] > 100:
                    break
                else:
                    reg.append(matrix[i_curr, j_curr])
                    i_curr = i_curr
                    j_curr = j_curr - 1

            i_curr = i_index
            j_curr = j_index
            while True:
                if matrix[i_curr, j_curr] > 100:
                    break
                else:
                    reg.append(matrix[i_curr, j_curr])
                    i_curr = i_curr
                    j_curr = j_curr + 1
            i_index = i_index + 1
            if matrix[i_index, j_index] > 100:
                break
        if matrix[i_index, j_index + 1] < 100:
            j_index = j_index + 1
        elif matrix[i_index, j_index - 1] < 100:
            j_index = j_index - 1
        else:
            print(i_index, j_index)
            break
    return(reg)
