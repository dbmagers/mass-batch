import os

var_1 = ['a','b','c','d']

var_2 = ['m','n','o']

root = '/Magers'

try:

    for folders in var_1:
        for nestedfolder in var_2:
            os.makedirs(os.path.join(root,folders,nestedfolder))

    
except FileExistsError:
    print("file already exists")