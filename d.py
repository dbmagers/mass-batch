from ast import Continue
import os

var_1 = ['a','b','c','d','e','f']

var_2 = ['m','n','o']

root = '/Magers'


for folders in var_1:
    for nestedfolder in var_2:
        pwd = os.path.join(root,folders,nestedfolder)
        print(pwd)
        if os.path.isdir(pwd) == True:
            Continue
        else: 
            os.makedirs(pwd)